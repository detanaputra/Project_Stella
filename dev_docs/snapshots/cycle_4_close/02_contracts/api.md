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
    # BERTopic example: {'model': <BERTopic instance>, 'texts': [...], 'num_topics': 12,
    #                    'params': {...}, 'original_texts': [...],
    #                    'static_chart_paths': {...}, 'viz_files': {...}}

    model_info: Dict[str, str]
    # Algorithm info for reproducibility.
    # BERTopic example: {'algorithm': 'BERTopic', 'version': '0.17.4',
    #                    'params': '<str(params)>', 'num_documents': '524', 'num_topics': '12'}

    quality_metrics: Optional[Dict[str, float]] = None
    # Topic quality evaluation, computed by the pipeline after training (not by
    # the algorithm itself). One value per metric, averaged across topics.
    # Example: {'npmi': 0.12, 'c_v': 0.45, 'u_mass': -3.2, 'topic_diversity': 0.78}

    topic_labels: Optional[Dict[int, str]] = None
    # User-provided names/interpretations per topic, set via topic refinement
    # (v0.4.0, WP1). Maps topic_id -> label; shown in the topics table.
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

**BERTopic refinement** (v0.4.0, WP1): `BERTopicAlgorithm` adds `merge_topics(result, topic_ids)` and `delete_topics(result, topic_ids)` — both mutate the model via BERTopic's native `merge_topics`/`delete_topics` and return an updated `TopicResult` (documents of deleted topics → outlier -1).

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
        """Returns {'topics': path, 'heatmap': path, 'barchart': path, 'hierarchy': path,
        'term_rank': path} for BERTopic (real plots); {} if unsupported. Individual
        failures are skipped."""

    def open_visualization(self, file_path: str) -> None:
        """Open an HTML visualization in the default browser, served over a
        local http://localhost server (browsers handle http reliably; file://
        intermittently opens a blank tab)."""
```

---

### StaticVizConverter

**Location:** `app/models/services/static_viz.py`

Converts BERTopic's Plotly visualizations to static matplotlib figures for the
in-app viz tabs (v0.3.0, WP1). BERTopic's `visualize_*` return Plotly figures
only; `fig.to_dict()` exposes the rendered data, which is re-plotted with
matplotlib.

```python
def plotly_fig_to_mpl(fig_dict: Dict[str, Any], viz_name: Optional[str] = None,
                      figure: Optional[Figure] = None) -> Figure:
    """Render a Plotly figure dict (from fig.to_dict()) as a matplotlib Figure.
    Dispatches on trace type (scatter / heatmap / bar); traces on distinct axes
    become subplots (BERTopic's barchart). viz_name enables per-viz styling
    (topics/hierarchy axis removal, term-rank axis labels)."""

def static_chart(model, viz_name: str, figure: Optional[Figure] = None) -> Figure:
    """Generate a static matplotlib chart for a BERTopic visualization by name
    (topics / heatmap / barchart / hierarchy / term_rank), passing viz_name
    through for per-visualisation styling."""

def save_static_charts(model, output_dir: str) -> Dict[str, str]:
    """Generate all 5 static charts and save them as PNG files; returns
    {viz_name: png_path}. Individual failures are skipped."""
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

    # Visualization (static charts + interactive HTML)
    def get_static_chart_path(self, viz_name: str) -> Optional[str]:
        """Return the pre-generated static chart PNG path for a visualization,
        or None if no result/chart exists."""

    def open_interactive_viz(self, viz_name: str) -> None:
        """Open the pre-generated offline HTML for a visualization in the
        default browser (the "Open interactive" button on the static viz tabs)."""

    # Topic refinement (v0.4.0, WP1)
    def merge_topics(self, topic_ids: List[int]) -> None:
        """Merge the selected topics into one; re-derives metrics + viz in a
        background thread (the view shows the loading panel)."""

    def delete_topics(self, topic_ids: List[int]) -> None:
        """Delete the selected topics (documents → outlier -1); re-derives
        metrics + viz in a background thread."""

    def label_topic(self, topic_id: int, label: str) -> None:
        """Store a user interpretation for a topic (no model mutation; the
        topics table re-renders with the label)."""

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
        _execute_pipeline: load_texts -> TopicProcessor.process -> compute metrics ->
        generate visualisations (static PNGs + offline HTML) -> set current_result.
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
| `panels/summary_panel.py` | `SummaryPanel` | Result tables (topics, doc-topics); sentinel-guarded render; topic refinement toolbar + checkbox selection (v0.4.0 WP1); document search + Detail window (v0.4.0 WP4) |
| `panels/document_detail.py` | `DocumentDetailWindow` | Detail view for a document: all topic assignments + full text in a scrollable read-only Text (v0.4.0 WP4) |
| `panels/metric_panel.py` | `MetricPanel` | 4 topic quality gauges (NPMI, C_V, UMass, Topic Diversity) from `result.quality_metrics`; sentinel-guarded render |
| `panels/static_viz_panel.py` | `StaticVizPanel` | Displays the pre-generated static chart PNG per BERTopic visualization + "Open interactive" button (opens the pre-generated HTML) |
| `panels/algorithm_settings_panel.py` | `AlgorithmSettingsPanel` | Persistent left column: BERTopic/UMAP/HDBSCAN param sections; Retrain button; scrollable; re-renders only on structural change |
| `panels/loading_panel.py` | `LoadingPanel` | Modal overlay; auto-closes when `analysis_in_progress` → false |
| `panels/export_panel.py` | `ExportPanel` | CSV/JSON/report export + browser visualizations; shown in a File → Export dialog (v0.3.0 WP2) |
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
- **Services** — `DataLoader` (+ `ValidationResult`), `TopicProcessor`, `Exporter`, `TopicVisualizer`, `StaticVizConverter`, `ProjectService`, `topic_quality` (`compute_topic_quality`).
- **Controllers** — `AppController` (project/params/export/persistence/visualization), `AnalysisController` (background training).
- **Views** — read-only panels that call controllers; no direct state mutation, file I/O, or algorithm calls.
- **Extending** — implement `BaseAlgorithm` + register; forms auto-generate from the schema.
