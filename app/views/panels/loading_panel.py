import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import Toplevel
from app.models.app_state import AppState
from app.controllers.app_controller import AppController
from app.views.window_utils import center_on_parent

class LoadingPanel(Toplevel):
    """
    A modal loading panel that displays the progress of the analysis.
    Automatically closes when analysis_in_progress becomes False.
    """
    def __init__(self, parent, state: AppState, controller: AppController):
        super().__init__(parent)
        self.title("Processing...")
        self.withdraw()  # keep hidden until positioned (v0.4.0, WP3)
        self.resizable(False, False)

        # Modal behavior
        self.transient(parent)

        self.appState: AppState = state
        self.controller = controller

        self._build_ui()

        # Position centered on the main window, then show (v0.4.0, WP3).
        center_on_parent(self, parent, 400, 200)
        self.deiconify()
        self.grab_set()

        # Subscribe to state changes to update status and check for completion
        self.appState.subscribe(self._on_state_changed)

    def _build_ui(self):
        container = ttk.Frame(self, padding=30)
        container.pack(fill=BOTH, expand=YES)

        self.lbl_status = ttk.Label(
            container,
            text=self.appState.analysis_status or "Starting analysis...",
            font=("Helvetica", 11),
            justify=CENTER
        )
        self.lbl_status.pack(pady=(0, 20))

        self.progress_bar = ttk.Progressbar(
            container,
            mode="indeterminate",
            bootstyle="success"
        )
        self.progress_bar.pack(fill=X, pady=10)
        self.progress_bar.start(10)

        ttk.Label(
            container,
            text="Please wait while we process your documents...",
            font=("Helvetica", 9, "italic"),
            bootstyle="secondary"
        ).pack(pady=20)

    def _on_state_changed(self, state: AppState):
        """Update status label and close the panel if analysis is complete."""
        # Check if the widget still exists to avoid "invalid command name" errors
        if not self.winfo_exists():
            return

        # Update status text
        if state.analysis_status:
            self.lbl_status.config(text=state.analysis_status)

        # Close panel if analysis finished (or failed)
        if not state.analysis_in_progress:
            self.destroy()
