# API Reference — Component Contracts

This document defines the interfaces and contracts for key components. Use these as specifications when implementing or generating code.

All package imports use the `app.` prefix (the package root is `app/`).

---

## Models

### TopicResult

**Location:** `app/models/topic_result.py`

Standardized output format returned by all algorithms.

```python
@dataclass
class TopicResult:
    """Standardized topic modelling output across all algorithms"""

    topics: List[Dict[str, float]]
    # List of topics; each topic is a dict mapping term → weight.
    # Example: [{"climate": 0.12, "environmental": 0.11, "carbon": 0.10, ...}, ...]

    doc_topics: List[Dict[int, float]]
    # List of document-topic assignments; each doc maps topic_id → probability.
    # Example: [{0: 0.85, 2: 0.15}, {1: 0.70, 3: 0.30}, ...]

    metadata: Dict[str, Any]
    # Algorithm-specific metadata.
    # BERTopic example: {'model': <BERTopic instance>, 'texts': [...], 'num_topics': 12}

    model_info: Dict[str, str]
    # Algorithm info for reproducibility.
    # BERTopic example: {'algorithm': 'BERTopic', 'version': '0.17.4',
    #                    'params': '<str(params)>', 'num_documents': '524', 'num_topics': '12'}

    quality_metrics: Optional[Dict[str, float]] = None
    # Topic quality evaluation, computed by the pipeline after training (not by
    # the algorithm itself). One value per metric, averaged across topics.
    # Example: {'npmi': 0.12, 'c_v': 0.45, 'u_mass': -3.2, 'topic_diversity': 0.78}
```

---

### AppState

**Location:** `app/models/app_state.py`

Centralized application state. Uses a **thread-safe event queue** for notifications so Tkinter updates happen on the main thread.

```python
@dataclass
class AppState:
    # INPUT STATE
    selected_file_path: Optional[str] = None
    file_preview: List[str] = field(default_factory=list)

    # ALGORITHM & PARAMETERS STATE
    selected_algorithm: str = "BERTopic"
    algorithm_params: Dict[str, Any] = field(default_factory=dict)

    # ANALYSIS STATE
    current_result: Optional[TopicResult] = None
    analysis_in_progress: bool = False
    analysis_progress: str = ""      # e.g., "70%"
    analysis_status: str = ""        # e.g., "Training model..."
    analysis_error: Optional[str] = None

    # Observer + thread-safety internals
    _observers: List[weakref.WeakMethod]   # weak refs; dead ones pruned in process_events
    event_queue: queue.Queue               # "STATE_CHANGED" events from notify()
    ui_callbacks: queue.Queue              # main-thread callables from call_on_main()

    def subscribe(self, callback: Callable[['AppState'], None]) -> None:
        """Register a view callback. Bound methods are wrapped in weakref.WeakMethod
        so destroyed widgets are garbage-collected (no memory leak)."""

    def notify(self) -> None:
        """Signal a state change. Does NOT call observers directly — it pushes
        "STATE_CHANGED" to event_queue. Observers run later on the main thread
        via process_events() (thread-safe UI dispatch)."""

    def call_on_main(self, callback: Callable[[], None]) -> None:
        """Queue a callable to run on the main thread. Worker threads must call
        this (not Tkinter directly); process_events() executes it (audit M1)."""

    def process_events(self) -> None:
        """Main-thread poll: run queued ui_callbacks, then drain event_queue and
        invoke live observers (pruning dead weak references). Scheduled by
        MainWindow._poll_state_events every 100 ms."""
```

---

### BaseAlgorithm

**Location:** `app/models/algorithms/base_algorithm.py`

Abstract interface all topic modelling algorithms must implement.

```python
class BaseAlgorithm(ABC):
    @abstractmethod
    def train(self, texts: List[str], **params) -> TopicResult:
        """Train on texts. Raises ValueError on invalid params, RuntimeError on failure."""

    @abstractmethod
    def get_default_params(self) -> Dict[str, Any]:
        """Dict mapping param_name -> default_value (the values shown in the UI)."""

    @abstractmethod
    def get_param_schema(self) -> Dict[str, Dict[str, Any]]:
        """Dict mapping param_name -> {'type', 'min', 'max', 'default', 'options', 'tooltip'}.
        Used by AppController.get_param_schema for generic parameter-form generation."""

    @property
    @abstractmethod
    def algorithm_name(self) -> str:
        """Human-readable name, e.g. "BERTopic"."""
```

**Registered algorithms** (`app/models/algorithms/__init__.py`): `AVAILABLE_ALGORITHMS = {'BERTopic': BERTopicAlgorithm}`. Only BERTopic is registered today; `get_algorithm(name)` raises `ValueError` for unknown names.

---

## Services

### DataLoader

**Location:** `app/models/services/data_loader.py`

File I/O, validation, and research guidance.

```python
@dataclass
class ValidationResult:
    is_valid: bool
    warnings: List[str] = field(default_factory=list)   # research guidance messages
    error: Optional[str] = None                          # message when is_valid is False

class DataLoader:
    def validate_file(self, file_path: str) -> ValidationResult:
        """Validate existence, format (.csv/.txt), readability; add sample-size
        and average-length research guidance as warnings. Does NOT raise."""

    def load_preview(self, file_path: str, n_lines: int = 10) -> List[str]:
        """Return the first N text lines (the picked text column for CSV). Raises ValueError."""

    def load_texts(self, file_path: str) -> List[str]:
        """Load all documents; drops NaN/empty/whitespace-only rows. Raises ValueError."""
```

---

### TopicProcessor

**Location:** `app/models/services/processor.py`

```python
class TopicProcessor:
    def __init__(self, algorithm: BaseAlgorithm): ...

    def process(
        self,
        texts: List[str],
        preprocessing_options: Dict[str, Any],     # remove_urls/remove_numbers/remove_emails/custom_stopwords_path
        model_params: Dict[str, Any],
        progress_callback: Optional[Callable[[str], None]] = None
    ) -> TopicResult:
        """Preprocess (noise filtering + custom stop-words) then train via algorithm.train.
        progress_callback receives stage strings ("Preprocessing text...", "Training model...",
        "Training Done") that the controller maps to milestone percentages."""
```

---

### Exporter

**Location:** `app/models/services/exporter.py`

```python
class Exporter:
    def to_csv(self, result: TopicResult, output_path: str) -> str:  ...
    def to_json(self, result: TopicResult, output_path: str) -> str: ...
    def generate_methodology_report(self, result: TopicResult, output_path: str) -> str:
        """Markdown report for academic reproducibility from result.model_info."""
```

---

### TopicVisualizer

**Location:** `app/models/services/visualizer.py`

Generates **offline** Plotly HTML visualizations (plotly.js embedded, no CDN).

```python
class TopicVisualizer:
    def __init__(self, output_dir: Optional[str] = None):
        # default: ~/.bertopic-gui/viz

    def visualize(self, result: TopicResult, algorithm_name: str) -> Dict[str, str]:
        """Returns {'topics': path, 'heatmap': path, 'barchart': path, 'hierarchy': path}
        for BERTopic (real plots); {} if unsupported. Individual failures are skipped."""

    def open_visualization(self, file_path: str) -> None:
        """Open an HTML visualization in the default browser."""
```

---

### ProjectService

**Location:** `app/models/services/project_service.py`

```python
class ProjectService:
    def save_project(self, state: AppState, output_path: str) -> str:
        """Serialize selected_file_path, selected_algorithm, algorithm_params, and
        result_metadata (NOT the model) to a JSON `.stella` file."""

    def load_project(self, input_path: str, state: AppState) -> None:
        """Deserialize into state; validates the algorithm name (falls back to
        BERTopic), merges params over defaults, clears non-existent file paths,
        and resets current_result to None (the model object cannot be restored)."""
```

---

## Controllers

Controllers own state changes and orchestrate services. **Views never mutate `AppState`; they call these methods and the controller updates state + calls `state.notify()`.**

### AppController

**Location:** `app/controllers/app_controller.py`

```python
class AppController:
    def __init__(self, state: AppState): ...

    # Project / file / algorithm / params
    def on_file_selected(self, file_path: str) -> None:
        """Validate via DataLoader; on success set selected_file_path + file_preview.
        On failure set analysis_error. Notifies."""

    def on_algorithm_changed(self, algorithm_name: str) -> None:
        """Reset selected_algorithm + algorithm_params to the algorithm's defaults."""

    def on_param_changed(self, param_name: str, value: Any) -> None: ...
    def set_params(self, params: Dict[str, Any]) -> None:
        """Batch-apply parameter values (wizard Train, custom mode)."""

    def get_param_schema(self, algorithm_name: str) -> Dict[str, Any]:
        """Expose an algorithm's schema to views (views never call the model directly)."""

    # Visualization (owns all model/file/process logic)
    def request_visualization(self, method_name: str, title: str) -> None:
        """Set analysis_in_progress + status, then run _generate_visualization on a
        background thread. Webview is launched in a separate process."""

    # Export
    def export_csv(self, output_path: str) -> None: ...
    def export_json(self, output_path: str) -> None: ...
    def export_methodology_report(self, output_path: str) -> None: ...
    def export_visualizations(self) -> Optional[str]:
        """Generate offline HTML via TopicVisualizer and open in the browser.
        Returns an error string or None. Safe from a background thread."""

    # Persistence
    def save_project(self, output_path: str) -> None: ...
    def load_project(self, input_path: str) -> None: ...
```

### AnalysisController

**Location:** `app/controllers/analysis_controller.py`

```python
class AnalysisController:
    def __init__(self, state: AppState): ...

    def run_analysis(self) -> None:
        """Re-entrancy guard (returns if analysis_in_progress). Validates a file is
        selected, sets analysis_in_progress, and starts a background thread running
        _execute_pipeline: load_texts -> TopicProcessor.process -> set current_result.
        Worker thread updates state via notify()/call_on_main (never Tkinter directly)."""
```

---

## Views

All views follow the same contract:
- Constructor: `(parent, state: AppState, controller: AppController, ...)` — receive the state and controller.
- Subscribe with `state.subscribe(self._on_state_changed)` where relevant.
- **Read-only:** read `state`, call `controller.*` methods. **Never mutate state, never do file I/O, never call algorithms/models directly.**

### Actual panels (`app/views/`)

| File | Class | Role |
|---|---|---|
| `panels/toolbox_panel.py` | `ToolboxPanel` | Left column: embeds `BERTopicVisualisation` |
| `panels/summary_panel.py` | `SummaryPanel` | Result tables (topics, doc-topics); sentinel-guarded render |
| `panels/algorithm_settings_panel.py` | `AlgorithmSettingsPanel` | BERTopic/UMAP/HDBSCAN param sections; Retrain button; scrollable; re-renders only on structural change |
| `panels/loading_panel.py` | `LoadingPanel` | Modal overlay; auto-closes when `analysis_in_progress` → false |
| `panels/export_panel.py` | `ExportPanel` | CSV/JSON/report export + browser visualizations |
| `panels/visualizations/bertopic_viz_panel.py` | `BERTopicVisualisation` | Thin: shows loading, calls `controller.request_visualization` |
| `wizard/wizard_main.py` + `panel_*.py` | `TopicModelWizard` etc. | 4-step setup wizard (algorithm/file → hyperparameters → preview → summary) |

The wizard's `_handle_train` syncs values **through the controller** (`on_file_selected`, `on_algorithm_changed`, `set_params`) before calling `analysis_controller.run_analysis()`.

---

## Extending: Adding a New Algorithm (e.g., LDA)

1. **Create** `app/models/algorithms/lda.py` with an `LDAAlgorithm(BaseAlgorithm)` implementing `train`, `get_default_params`, `get_param_schema`, `algorithm_name`.
2. **Register** in `app/models/algorithms/__init__.py`:
   ```python
   AVAILABLE_ALGORITHMS = {
       'BERTopic': BERTopicAlgorithm,
       'LDA': LDAAlgorithm,
   }
   ```
3. **No UI changes needed.** The parameter form is generated from `get_param_schema` via the controller, and the modular sections already follow the `on_param_changed` contract.

---

## Summary

- **Models** — `TopicResult`, `AppState` (thread-safe event-queue notifications), `BaseAlgorithm` + BERTopic.
- **Services** — `DataLoader` (+ `ValidationResult`), `TopicProcessor`, `Exporter`, `TopicVisualizer`, `ProjectService`.
- **Controllers** — `AppController` (project/params/export/persistence/visualization), `AnalysisController` (background training).
- **Views** — read-only panels that call controllers; no direct state mutation, file I/O, or algorithm calls.
- **Extending** — implement `BaseAlgorithm` + register; forms auto-generate from the schema.
