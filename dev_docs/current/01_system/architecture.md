# Architecture Guide — MVC Patterns & Data Flows

This document provides detailed MVC architecture, data flow examples, and implementation patterns. Reference this when building components.

> **Repo layout:** the current file/folder structure is maintained in `dev_docs/03_control/repository_structure.md` (it evolves; a fixed tree here would drift).

---

## Core Pattern: AppState with Observers

**AppState** is the single source of truth. All state lives here. Views observe it.

```python
# app/models/app_state.py
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List, Callable

@dataclass
class AppState:
    # Input
    selected_file_path: Optional[str] = None
    file_preview: List[str] = field(default_factory=list)
    
    # Algorithm & parameters
    selected_algorithm: str = "BERTopic"
    algorithm_params: Dict[str, Any] = field(default_factory=dict)
    
    # Analysis results
    current_result: Optional['TopicResult'] = None
    analysis_in_progress: bool = False
    analysis_progress: str = ""  # e.g., "30%"
    analysis_error: Optional[str] = None
    
    # Observers (views subscribe here)
    _observers: List[Callable[['AppState'], None]] = field(
        default_factory=list, 
        init=False, 
        repr=False
    )
    
    def subscribe(self, callback: Callable[['AppState'], None]):
        """Views call this: state.subscribe(my_panel._on_state_changed)"""
        self._observers.append(callback)
    
    def notify(self):
        """Controllers call this after state changes"""
        for callback in self._observers:
            callback(self)
```

**Why this pattern:**
- Single source of truth (no duplicate state in views)
- Observer pattern decouples views from controllers
- Easy to test (mock AppState, verify controller updates)
- Easy to extend (add new state properties)
- Easy to persist (serialize AppState for save/load)

---

## Data Flow Examples

### Flow 1: User Uploads File

```
USER ACTION:
  Browses for a file in the wizard's AlgorithmPanel ("Browse" button)

VIEW (AlgorithmPanel)
  → Calls: controller.on_file_selected(file_path)

CONTROLLER (AppController)
  → Calls: DataLoader.validate_file(path) -> ValidationResult
  → Calls: DataLoader.load_preview(path)
  → Updates: state.selected_file_path = path
  → Updates: state.file_preview = preview
  → Calls: state.notify()

MODEL (AppState notifies all subscribers via the event queue)
  → Calls: subscribed panels re-render (e.g. wizard preview step)

VIEW (preview step re-renders)
  → Reads: state.selected_file_path
  → Reads: state.file_preview
  → Displays the preview (no file I/O in the view — it comes from state)
```

**Key points:**
- Controller calls DataLoader (model service)
- Controller updates AppState (model)
- Controller calls state.notify() (triggers view updates)
- Views read from state (pull, not push)

---

### Flow 2: User Changes Algorithm

```
USER ACTION:
  Selects "BERTopic" from algorithm dropdown in the wizard's AlgorithmPanel
  (only BERTopic is registered in AVAILABLE_ALGORITHMS today)

VIEW (AlgorithmPanel)
  → Calls: controller.on_algorithm_changed("BERTopic")

CONTROLLER (AppController)
  → Calls: get_algorithm("BERTopic")
  → Gets: default_params = BERTopicAlgorithm.get_default_params()
  → Updates: state.selected_algorithm = "BERTopic"
  → Updates: state.algorithm_params = default_params
  → Calls: state.notify()

MODEL (AppState notifies all subscribers via the event queue)
  → Calls: AlgorithmSettingsPanel._on_state_changed(state)

VIEW (AlgorithmSettingsPanel re-renders, structural change only)
  → Reads: state.selected_algorithm
  → DESTROYS old parameter section widgets
  → CREATES modular sections for BERTopic/UMAP/HDBSCAN parameters
```

**Key points:**
- Dynamic UI regeneration (same panel, different form)
- Parameter schema drives form generation (fetched via `controller.get_param_schema()`)
- No hardcoded parameter logic in views; views never call `get_algorithm` directly

---

### Flow 3: User Runs Analysis

```
USER ACTION:
  Clicks "Train" in the wizard, or "Retrain Model with Current Params" in the
  AlgorithmSettingsPanel (there is no ProcessingPanel)

VIEW (wizard / AlgorithmSettingsPanel)
  → Syncs values through the controller (on_file_selected / on_algorithm_changed / set_params)
  → Shows the LoadingPanel (owned by MainWindow)
  → Calls: analysis_controller.run_analysis()

CONTROLLER (AnalysisController)
  → Re-entrancy guard: returns if state.analysis_in_progress
  → Sets: state.analysis_in_progress = True
  → Starts background thread (_execute_pipeline)

  [Background thread]
  → Sets: state.analysis_progress = "0%"
  → Gets: texts = DataLoader.load_texts(state.selected_file_path)
  → Gets: algo = get_algorithm(state.selected_algorithm)
  → Creates: processor = TopicProcessor(algo)
  → Calls: result = processor.process(
      texts, preprocessing_options, model_params=state.algorithm_params,
      progress_callback=update_progress)
  → On completion:
    → Updates: state.current_result = result
    → Updates: state.analysis_in_progress = False
    → Updates: state.analysis_progress = "100%"
    → Updates: state.analysis_status = "Analysis complete!"
    → Calls: state.notify()

MODEL (AppState notifies via the event queue; process_events dispatches on the main thread)
  → Calls: SummaryPanel._on_state_changed(state)
  → Calls: LoadingPanel (auto-closes when analysis_in_progress → false)
  → Calls: AlgorithmSettingsPanel._on_state_changed(state)

VIEW (SummaryPanel re-renders)
  → Reads: state.current_result
  → IF result exists:
    → Displays topic tables and per-document assignments
  → Else: Shows "No results yet"
```

**Key points:**
- Threading happens in the controller (views never block); worker threads reach the UI only via `AppState.call_on_main` / `process_events` on the main thread
- Progress updates trigger view re-renders
- Multiple views react to a single state change
- Views only read state and call controllers — they never call algorithms or load files directly

---

## MVC Layers Explained

### MODEL Layer (app/models/)

**Responsibility:** Data structures, business logic, NO UI imports

**What belongs here:**
- AppState (state machine)
- TopicResult (standardized output)
- BaseAlgorithm (abstract interface)
- Algorithm implementations (BERTopic today; LDA/NMF planned)
- Services (DataLoader, Processor, Exporter, Visualizer)

**What DOESN'T belong here:**
- No ttkbootstrap imports
- No GUI logic
- No view state

**Testing:** Can test entirely with unit tests (no GUI needed)

**Reusability:** Could be reused in web/CLI version without changes

---

### VIEW Layer (app/views/)

**Responsibility:** Display data, listen to state changes, delegate actions to controller

**What belongs here:**
- ttkbootstrap panels (ToolboxPanel, SummaryPanel, MetricPanel, AlgorithmSettingsPanel, LoadingPanel, ExportPanel, wizard panels)
- Layout & styling
- Widget creation
- Subscribe to AppState.subscribe()
- Call controller methods on user actions

**What DOESN'T belong here:**
- Algorithm logic
- File I/O
- Data processing
- Business logic of any kind

**Pattern:** Every panel follows this structure:

```python
class MyPanel(ttk.Frame):
    def __init__(self, parent, app_state: AppState, controller):
        super().__init__(parent)
        self.state = app_state
        self.controller = controller
        
        # Subscribe to state changes
        self.state.subscribe(self._on_state_changed)
        
        # Build static UI (called once)
        self._build_ui()
        
        # Initial render
        self._render()
    
    def _build_ui(self):
        """Create widgets (called once on init)"""
        self.label = ttk.Label(self, text="")
        self.label.pack()
        
        self.button = ttk.Button(self, text="Click me")
        self.button.pack()
        self.button.config(command=self._on_button_clicked)
    
    def _on_state_changed(self, state: AppState):
        """Called by AppState.notify() when state changes"""
        self._render()
    
    def _render(self):
        """Update display based on current state"""
        self.label.config(text=f"File: {self.state.selected_file_path}")
        self.button.config(state="normal" if self.state.selected_file_path else "disabled")
    
    def _on_button_clicked(self):
        """Handle user action - delegate to controller"""
        self.controller.on_some_action()
```

---

### CONTROLLER Layer (app/controllers/)

**Responsibility:** Orchestrate model and view. Handle user events.

**What belongs here:**
- Event handlers (on_file_selected, on_algorithm_changed, etc.)
- Call model services (DataLoader, Processor)
- Update AppState
- Call state.notify() to trigger view updates
- Threading (background jobs)
- Error handling

**What DOESN'T belong here:**
- Direct UI manipulation
- Algorithm implementations

**Pattern:** Controller methods handle one user action

```python
class AppController:
    def __init__(self, app_state: AppState):
        self.state = app_state
        self.loader = DataLoader()
    
    def on_file_selected(self, file_path: str):
        """Handle file selection"""
        try:
            # Validate & load
            preview = self.loader.load_preview(file_path)
            
            # Update state
            self.state.selected_file_path = file_path
            self.state.file_preview = preview
            self.state.analysis_error = None
            
            # Notify views
            self.state.notify()
        except FileNotFoundError as e:
            # Handle error
            self.state.analysis_error = f"File not found: {file_path}"
            self.state.notify()
        except Exception as e:
            # Handle unexpected error
            self.state.analysis_error = f"Error loading file: {str(e)}"
            self.state.notify()
    
    def on_algorithm_changed(self, algorithm_name: str):
        """Handle algorithm switch"""
        from algorithms import get_algorithm
        
        algo = get_algorithm(algorithm_name)
        self.state.selected_algorithm = algorithm_name
        self.state.algorithm_params = algo.get_default_params()
        self.state.notify()
    
    def on_param_changed(self, param_name: str, value: Any):
        """Handle parameter adjustment"""
        self.state.algorithm_params[param_name] = value
        self.state.notify()
```

---

## Algorithm-Agnostic Design

All algorithms follow the same interface (BaseAlgorithm). This allows UI to work with any algorithm without changes.

### BaseAlgorithm Contract

```python
# app/models/algorithms/base_algorithm.py
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from app.models.topic_result import TopicResult

class BaseAlgorithm(ABC):
    @abstractmethod
    def train(self, texts: List[str], **params) -> TopicResult:
        """
        Train model on texts with given parameters.
        
        Args:
            texts: List of documents to model
            **params: Algorithm-specific parameters
        
        Returns:
            TopicResult with standardized format
        """
        pass
    
    @abstractmethod
    def get_default_params(self) -> Dict[str, Any]:
        """
        Return default parameters for this algorithm.
        
        Returns:
            Dict like {'min_topic_size': 5, 'embedding_model': 'all-MiniLM-L6-v2'}
        """
        pass
    
    @abstractmethod
    def get_param_schema(self) -> Dict[str, Dict]:
        """
        Return parameter schema for UI form generation.
        
        Returns:
            Dict mapping param_name to {type, min, max, default, tooltip, options}
            
        Example:
            {
                'min_topic_size': {
                    'type': 'int',
                    'min': 2,
                    'max': 50,
                    'default': 5,
                    'tooltip': 'Minimum documents per topic'
                },
                'embedding_model': {
                    'type': 'choice',
                    'options': ['all-MiniLM-L6-v2', 'paraphrase-MiniLM-L6-v2'],
                    'default': 'all-MiniLM-L6-v2',
                    'tooltip': 'Embedding model to use'
                }
            }
        """
        pass
    
    @property
    def algorithm_name(self) -> str:
        """Return human-readable algorithm name"""
        pass
```

### Registry Pattern

```python
# app/models/algorithms/__init__.py
from .bertopic import BERTopicAlgorithm

AVAILABLE_ALGORITHMS = {
    'BERTopic': BERTopicAlgorithm,
    # Future: 'LDA': LDAAlgorithm, 'NMF': NMFAlgorithm
}

def get_algorithm(name: str) -> BaseAlgorithm:
    """Factory function to get algorithm instance"""
    if name not in AVAILABLE_ALGORITHMS:
        raise ValueError(f"Unknown algorithm: {name}")
    return AVAILABLE_ALGORITHMS[name]()
```

**Extending:** To add a new algorithm (e.g., NMF):
1. Create `app/models/algorithms/nmf.py` with NMFAlgorithm class
2. Implement BaseAlgorithm methods
3. Add to AVAILABLE_ALGORITHMS registry
4. No UI changes needed (the parameter form is generated from the algorithm's schema via the controller)

---

## Key MVC Principles

1. **Models know nothing about views** — No ttkbootstrap imports in `app/models/`
2. **Views know nothing about business logic** — No algorithms or file I/O in `app/views/`
3. **Controllers orchestrate** — Controllers call models and update state; views observe
4. **State flows one direction** — Models → AppState → Views (via subscription)
5. **Events flow opposite way** — View clicks → Controller → Models/AppState
6. **Views are read-only** — Views read state, never modify it directly
7. **Controller is the only modifier** — Only controller changes AppState

---

## Testing Strategy (Unit Tests)

> **Status:** no committed `tests/` suite exists yet. Correctness is verified with ad-hoc headless smoke tests (e.g. after the M-fix batch in the v0.1.1 audit) and the occasional live-Tk check. A proper `tests/` tree is planned; the intended layout is described below.

The MODEL layer is unit-testable without a GUI (no ttkbootstrap imports), so tests can run headless:
- **AppState** — subscription, notification, and the event-queue dispatch (`notify()` → `process_events()`).
- **DataLoader** — `load_texts`, `load_preview`, `validate_file` (returning `ValidationResult`).
- **BERTopicAlgorithm** — train on a small corpus and check the `TopicResult` shape.
- **Controllers** — `AppController.on_file_selected` / `on_algorithm_changed`, `AnalysisController.run_analysis` against a stub `AppState`.
- **Views** — would need a mocked state; deferred until the suite is added.

---

## Summary

- **MODEL** = Data + business logic (testable, reusable)
- **VIEW** = Display + listen (dumb, read-only)
- **CONTROLLER** = Orchestration + events (glue between model & view)
- **AppState** = Single source of truth (observer pattern)
- **Observer pattern** = Views subscribe to state changes

This pattern scales to LDA/NMF/Top2Vec without UI changes.
