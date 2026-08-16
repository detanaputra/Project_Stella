# Architecture Guide — MVC Patterns & Data Flows

This document provides detailed MVC architecture, data flow examples, and implementation patterns. Reference this when building components.

---

## Folder Structure (MVC)

```
Project_Stella/
├── main.py                           # Entry point
├── requirements.txt
├── claude.md                         # High-level context
├── ARCHITECTURE.md                   # This file
├── API.md                            # Component contracts
├── DEVELOPMENT.md                    # Setup & testing
│
├── models/                           # MODEL: Data & business logic (no UI)
│   ├── __init__.py
│   ├── topic_result.py              # TopicResult dataclass
│   ├── app_state.py                 # AppState with observer pattern
│   │
│   ├── algorithms/
│   │   ├── __init__.py              # AVAILABLE_ALGORITHMS registry
│   │   ├── base_algorithm.py        # Abstract BaseAlgorithm class
│   │   ├── bertopic.py              # BERTopic implementation
│   │   ├── lda.py                   # [Future] LDA
│   │   └── nmf.py                   # [Future] NMF
│   │
│   └── services/
│       ├── __init__.py
│       ├── data_loader.py           # File I/O, validation, preprocessing
│       ├── processor.py             # Unified processing pipeline
│       ├── exporter.py              # CSV, JSON export
│       └── visualizer.py            # Plotly HTML export
│
├── views/                            # VIEW: ttkbootstrap UI (display only)
│   ├── __init__.py
│   ├── main_window.py               # Main app window & layout
│   ├── panels/
│   │   ├── __init__.py
│   │   ├── input_panel.py           # File upload UI
│   │   ├── settings_panel.py        # Dynamic parameter form
│   │   ├── processing_panel.py      # Progress display
│   │   └── results_panel.py         # Results display
│   └── styles/
│       └── theme.py                 # ttkbootstrap theme config
│
├── controllers/                      # CONTROLLER: Orchestration
│   ├── __init__.py
│   ├── app_controller.py            # Main app event handlers
│   └── analysis_controller.py       # Training pipeline
│
├── utils/
│   ├── __init__.py
│   ├── constants.py                 # App constants
│   ├── logger.py                    # Logging setup
│   └── validators.py                # Input validation helpers
│
└── tests/                            # Unit tests (mirrors src)
    ├── test_models/
    ├── test_services/
    ├── test_controllers/
    └── fixtures/
```

---

## Core Pattern: AppState with Observers

**AppState** is the single source of truth. All state lives here. Views observe it.

```python
# models/app_state.py
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
  Clicks "Select File" button in InputPanel

VIEW (InputPanel)
  → Calls: controller.on_file_selected(file_path)

CONTROLLER (AppController)
  → Calls: DataLoader.validate_file(path)
  → Calls: DataLoader.load_preview(path)
  → Updates: state.selected_file_path = path
  → Updates: state.file_preview = preview
  → Calls: state.notify()

MODEL (AppState notifies all subscribers)
  → Calls: InputPanel._on_state_changed(state)
  → Calls: SettingsPanel._on_state_changed(state)
  → etc. (all subscribed views)

VIEW (InputPanel re-renders)
  → Reads: state.selected_file_path
  → Reads: state.file_preview
  → Displays file name & preview
  → Enables "Run Analysis" button
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
  Selects "LDA" from algorithm dropdown in SettingsPanel

VIEW (SettingsPanel)
  → Calls: controller.on_algorithm_changed("LDA")

CONTROLLER (AppController)
  → Calls: get_algorithm("LDA")
  → Gets: default_params = LDA.get_default_params()
  → Gets: param_schema = LDA.get_param_schema()
  → Updates: state.selected_algorithm = "LDA"
  → Updates: state.algorithm_params = default_params
  → Calls: state.notify()

MODEL (AppState notifies all subscribers)
  → Calls: SettingsPanel._on_state_changed(state)

VIEW (SettingsPanel re-renders)
  → Reads: state.selected_algorithm
  → Reads: param_schema from LDA.get_param_schema()
  → DESTROYS old parameter widgets
  → CREATES new widgets for LDA params (alpha, beta, etc.)
  → Now shows LDA-specific form
```

**Key points:**
- Dynamic UI regeneration (same panel, different form)
- Algorithm schema drives parameter form generation
- No hardcoded parameter logic in views

---

### Flow 3: User Runs Analysis

```
USER ACTION:
  Clicks "Run Analysis" button in ProcessingPanel

VIEW (ProcessingPanel)
  → Calls: controller.on_run_analysis()

CONTROLLER (AnalysisController)
  → Starts background thread (non-blocking UI)
  → Updates: state.analysis_in_progress = True
  → Updates: state.analysis_progress = "0%"
  → Calls: state.notify()
  
  [Background thread]
  → Gets: texts = DataLoader.load(state.selected_file_path)
  → Gets: algo = get_algorithm(state.selected_algorithm)
  → Calls: result = algo.train(texts, **state.algorithm_params)
  → For each progress event:
    → Updates: state.analysis_progress = "30%"
    → Calls: state.notify()
  → On completion:
    → Updates: state.current_result = result
    → Updates: state.analysis_in_progress = False
    → Updates: state.analysis_progress = "100%"
    → Calls: state.notify()

MODEL (AppState notifies)
  → Calls: ProcessingPanel._on_state_changed(state)
  → Calls: ResultsPanel._on_state_changed(state)

VIEW (ProcessingPanel re-renders)
  → Reads: state.analysis_in_progress
  → Reads: state.analysis_progress
  → Shows/hides progress bar
  → Displays "Training... 30%"

VIEW (ResultsPanel re-renders)
  → Reads: state.current_result
  → IF result exists:
    → Displays topics table
    → Displays stats cards
    → Shows action buttons
  → Else: Shows "No results yet"
```

**Key points:**
- Threading happens in controller (views never block)
- Progress updates trigger view re-renders
- Multiple views react to single state change
- View only reads, never calls algorithms

---

## MVC Layers Explained

### MODEL Layer (models/)

**Responsibility:** Data structures, business logic, NO UI imports

**What belongs here:**
- AppState (state machine)
- TopicResult (standardized output)
- BaseAlgorithm (abstract interface)
- Algorithm implementations (BERTopic, LDA, etc.)
- Services (DataLoader, Processor, Exporter, Visualizer)

**What DOESN'T belong here:**
- No ttkbootstrap imports
- No GUI logic
- No view state

**Testing:** Can test entirely with unit tests (no GUI needed)

**Reusability:** Could be reused in web/CLI version without changes

---

### VIEW Layer (views/)

**Responsibility:** Display data, listen to state changes, delegate actions to controller

**What belongs here:**
- ttkbootstrap panels (InputPanel, SettingsPanel, etc.)
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

### CONTROLLER Layer (controllers/)

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
# models/algorithms/base_algorithm.py
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from models.topic_result import TopicResult

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
# models/algorithms/__init__.py
from .bertopic import BERTopicAlgorithm
from .lda import LDAAlgorithm

AVAILABLE_ALGORITHMS = {
    'BERTopic': BERTopicAlgorithm,
    'LDA': LDAAlgorithm,
    # Add more as you implement them
}

def get_algorithm(name: str) -> BaseAlgorithm:
    """Factory function to get algorithm instance"""
    if name not in AVAILABLE_ALGORITHMS:
        raise ValueError(f"Unknown algorithm: {name}")
    return AVAILABLE_ALGORITHMS[name]()
```

**Extending:** To add a new algorithm (e.g., NMF):
1. Create `models/algorithms/nmf.py` with NMFAlgorithm class
2. Implement BaseAlgorithm methods
3. Add to AVAILABLE_ALGORITHMS registry
4. No UI changes needed (parameter form auto-generates)

---

## Key MVC Principles

1. **Models know nothing about views** — No ttkbootstrap imports in models/
2. **Views know nothing about business logic** — No algorithms or file I/O in views/
3. **Controllers orchestrate** — Controllers call models and update state; views observe
4. **State flows one direction** — Models → AppState → Views (via subscription)
5. **Events flow opposite way** — View clicks → Controller → Models/AppState
6. **Views are read-only** — Views read state, never modify it directly
7. **Controller is the only modifier** — Only controller changes AppState

---

## Testing Strategy (Unit Tests)

### Test Models (No UI needed)

```python
# tests/test_models/test_app_state.py
def test_app_state_subscribe():
    state = AppState()
    called = []
    state.subscribe(lambda s: called.append(s))
    
    state.selected_file_path = "test.csv"
    state.notify()
    
    assert len(called) == 1
    assert called[0].selected_file_path == "test.csv"

# tests/test_models/test_algorithms/test_bertopic.py
def test_bertopic_train():
    algo = BERTopicAlgorithm()
    texts = ["hello world", "goodbye world"]
    result = algo.train(texts, min_topic_size=2)
    
    assert isinstance(result, TopicResult)
    assert len(result.topics) > 0
    assert len(result.doc_topics) == 2
```

### Test Controllers (No UI needed)

```python
# tests/test_controllers/test_app_controller.py
def test_on_file_selected():
    state = AppState()
    controller = AppController(state)
    
    controller.on_file_selected("tests/fixtures/sample_data.csv")
    
    assert state.selected_file_path == "tests/fixtures/sample_data.csv"
    assert len(state.file_preview) > 0
```

### Test Views (Mock state)

```python
# tests/test_views/test_input_panel.py
def test_input_panel_renders_file():
    root = tk.Tk()
    state = AppState()
    state.selected_file_path = "test.csv"
    
    panel = InputPanel(root, state, controller=None)
    panel._render()
    
    # Verify panel shows file name
    # (check label text, button state, etc.)
```

---

## Summary

- **MODEL** = Data + business logic (testable, reusable)
- **VIEW** = Display + listen (dumb, read-only)
- **CONTROLLER** = Orchestration + events (glue between model & view)
- **AppState** = Single source of truth (observer pattern)
- **Observer pattern** = Views subscribe to state changes

This pattern scales to LDA/NMF/Top2Vec without UI changes.
