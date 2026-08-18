from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List, Callable
import queue
import traceback
import weakref
from app.models.topic_result import TopicResult

@dataclass
class AppState:
    """
    Single source of truth for entire app state.
    Uses a thread-safe queue for notifications to ensure Tkinter updates
    happen on the main thread.
    """
    # INPUT STATE
    selected_file_path: Optional[str] = None
    file_preview: List[str] = field(default_factory=list)

    # ALGORITHM & PARAMETERS STATE
    selected_algorithm: str = "BERTopic"
    algorithm_params: Dict[str, Any] = field(default_factory=dict)

    # ANALYSIS STATE
    current_result: Optional[TopicResult] = None  # Standardized output across algorithms
    analysis_in_progress: bool = False
    analysis_progress: str = ""  # e.g., "30%"
    analysis_status: str = ""    # e.g., "Extracting embeddings..."
    analysis_error: Optional[str] = None

    # Observer Pattern
    _observers: List[weakref.WeakMethod] = field(
        default_factory=list,
        init=False,
        repr=False
    )

    # Thread-safe event queue for UI notifications
    event_queue: queue.Queue = field(
        default_factory=queue.Queue,
        init=False,
        repr=False
    )

    # Thread-safe queue of callables to run on the main thread. Worker threads
    # must never call Tkinter directly; they schedule work here instead and
    # process_events() executes it on the main thread (audit M1).
    ui_callbacks: queue.Queue = field(
        default_factory=queue.Queue,
        init=False,
        repr=False
    )

    def subscribe(self, callback: Callable[['AppState'], None]) -> None:
        """Register a view callback to be notified on state changes."""
        if hasattr(callback, "__self__"):
            # It's a bound method, use WeakMethod
            self._observers.append(weakref.WeakMethod(callback))
        else:
            # It's a regular function, WeakMethod doesn't work,
            # but for GUI panels we expect bound methods.
            # We'll store it as is or wrap it.
            self._observers.append(callback)

    def notify(self) -> None:
        """
        Notify all subscribed views of state changes.
        Instead of calling observers directly, it pushes an event to the queue.
        """
        self.event_queue.put("STATE_CHANGED")

    def call_on_main(self, callback: Callable[[], None]) -> None:
        """
        Schedule a callable to run on the main thread.

        Safe to call from worker threads; process_events() executes the
        callable on the Tkinter main loop. Used to marshal Tkinter calls
        (dialogs, widget updates) off worker threads (audit M1).
        """
        self.ui_callbacks.put(callback)

    def process_events(self) -> None:
        """
        Called by the main window on the main thread to trigger observers.
        Cleans up dead weak references during the process.
        """
        # Run callables scheduled by worker threads on the main thread first
        # (audit M1). A modal dialog here blocks, but that is user interaction.
        try:
            while True:
                ui_callback = self.ui_callbacks.get_nowait()
                try:
                    ui_callback()
                except Exception:
                    traceback.print_exc()
        except queue.Empty:
            pass

        try:
            while True:
                event = self.event_queue.get_nowait()
                if event == "STATE_CHANGED":
                    # Filter out dead references and notify live ones
                    live_observers = []
                    for ref in self._observers:
                        callback = ref() if isinstance(ref, weakref.WeakMethod) else ref
                        if callback is None:
                            continue
                        try:
                            callback(self)
                        except Exception:
                            # One panel's render error must not break event
                            # polling for the rest of the app (audit H5).
                            traceback.print_exc()
                        live_observers.append(ref)

                    # Update observer list to remove dead references
                    self._observers = live_observers

                self.event_queue.task_done()
        except queue.Empty:
            pass
