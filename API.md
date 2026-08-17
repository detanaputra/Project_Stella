# API Reference — Component Contracts

This document defines the interfaces and contracts for key components. Use these as specifications when implementing or generating code.

---

## Models

### TopicResult

**Location:** `models/topic_result.py`

Standardized output format returned by all algorithms.

```python
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

@dataclass
class TopicResult:
    """Standardized topic modelling output across all algorithms"""
    
    topics: List[Dict[str, float]]
    """
    List of topics. Each topic is a dict mapping term → weight.
    Example:
    [
        {"climate": 0.12, "environmental": 0.11, "carbon": 0.10, ...},
        {"policy": 0.15, "government": 0.13, "legislation": 0.11, ...},
        ...
    ]
    """
    
    doc_topics: List[Dict[int, float]]
    """
    List of document-topic assignments.
    Each document maps topic_id → probability.
    Example:
    [
        {0: 0.85, 2: 0.15},  # Doc 0: 85% topic 0, 15% topic 2
        {1: 0.70, 3: 0.30},  # Doc 1: 70% topic 1, 30% topic 3
        ...
    ]
    """
    
    metadata: Dict[str, Any]
    """
    Algorithm-specific metadata. Example:
    {
        'model': <BERTopic instance>,
        'texts': [list of input texts],
        'embeddings': [numpy arrays],
        'cluster_info': {...}
    }
    """
    
    model_info: Dict[str, str]
    """
    Algorithm info for reproducibility. Example:
    {
        'algorithm': 'BERTopic',
        'version': '0.15.0',
        'params': {'min_topic_size': 5, 'embedding_model': 'all-MiniLM-L6-v2'},
        'training_time': '3m 42s',
        'num_documents': '524',
        'num_topics': '12'
    }
    """
```

---

### AppState

**Location:** `models/app_state.py`

Centralized application state machine.

```python
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List, Callable

@dataclass
class AppState:
    """Single source of truth for entire app state"""
    
    # INPUT STATE
    selected_file_path: Optional[str] = None
    file_preview: List[str] = field(default_factory=list)
    
    # ALGORITHM & PARAMETERS STATE
    selected_algorithm: str = "BERTopic"
    algorithm_params: Dict[str, Any] = field(default_factory=dict)
    
    # ANALYSIS STATE
    current_result: Optional[TopicResult] = None
    analysis_in_progress: bool = False
    analysis_progress: str = ""  # e.g., "30%"
    analysis_status: str = ""    # e.g., "Extracting embeddings..."
    analysis_error: Optional[str] = None
    
    # Observers (views)
    _observers: List[Callable[['AppState'], None]] = field(
        default_factory=list,
        init=False,
        repr=False
    )
    
    def subscribe(self, callback: Callable[['AppState'], None]) -> None:
        """
        Register a view callback to be notified on state changes.
        
        Args:
            callback: Function that takes AppState as argument
        
        Example:
            state.subscribe(my_panel._on_state_changed)
        """
        self._observers.append(callback)
    
    def notify(self) -> None:
        """
        Notify all subscribed views of state changes.
        Called by controller after updating state.
        
        Example:
            state.selected_algorithm = "LDA"
            state.notify()  # Triggers all callbacks
        """
        for callback in self._observers:
            callback(self)
```

---

### BaseAlgorithm

**Location:** `models/algorithms/base_algorithm.py`

Abstract base class for all topic modelling algorithms.

```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from models.topic_result import TopicResult

class BaseAlgorithm(ABC):
    """Abstract interface all topic modelling algorithms must implement"""
    
    @abstractmethod
    def train(self, texts: List[str], **params) -> TopicResult:
        """
        Train the algorithm on texts.
        
        Args:
            texts: List of documents (strings)
            **params: Algorithm-specific parameters (from AppState.algorithm_params)
        
        Returns:
            TopicResult with standardized format
        
        Raises:
            ValueError: If parameters invalid
            RuntimeError: If training fails
        """
        pass
    
    @abstractmethod
    def get_default_params(self) -> Dict[str, Any]:
        """
        Get default parameters for this algorithm.
        
        Returns:
            Dict mapping param_name → default_value
        
        Example:
            {
                'min_topic_size': 5,
                'embedding_model': 'all-MiniLM-L6-v2',
                'n_gram_range': (1, 2)
            }
        """
        pass
    
    @abstractmethod
    def get_param_schema(self) -> Dict[str, Dict[str, Any]]:
        """
        Get parameter schema for UI form generation.
        
        Returns:
            Dict mapping param_name → schema dict
            
        Schema dict structure:
            {
                'type': 'int' | 'float' | 'choice' | 'range',
                'min': number (for int/float),
                'max': number (for int/float),
                'default': value,
                'options': [list] (for choice type),
                'tooltip': 'Help text shown to user'
            }
        
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
                    'tooltip': 'Embedding model'
                }
            }
        """
        pass
    
    @property
    @abstractmethod
    def algorithm_name(self) -> str:
        """
        Human-readable algorithm name.
        
        Returns:
            String like "BERTopic", "LDA", "NMF"
        """
        pass
```

---

## Services

### DataLoader

**Location:** `models/services/data_loader.py`

File I/O, validation, and preprocessing.

```python
class DataLoader:
    """Load and validate input data"""
    
    def load_preview(self, file_path: str, n_lines: int = 10) -> List[str]:
        """
        Load preview of file (first N lines).
        
        Args:
            file_path: Path to CSV or TXT file
            n_lines: Number of lines to load
        
        Returns:
            List of text lines
        
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file format unsupported
        """
        pass
    
    def load_texts(self, file_path: str) -> List[str]:
        """
        Load all texts from file.
        
        Args:
            file_path: Path to CSV or TXT file
        
        Returns:
            List of documents
        
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file format unsupported
        """
        pass
    
    def validate_file(self, file_path: str) -> bool:
        """
        Validate file exists and is readable.
        
        Args:
            file_path: Path to file
        
        Returns:
            True if valid
        
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file format unsupported
        """
        pass
```

---

### Processor

**Location:** `models/services/processor.py`

Unified processing pipeline.

```python
class TopicProcessor:
    """Orchestrate model training and preprocessing"""
    
    def __init__(self, algorithm: BaseAlgorithm):
        """
        Args:
            algorithm: Instance of BaseAlgorithm subclass
        """
        pass
    
    def process(
        self,
        texts: List[str],
        preprocessing_options: Dict[str, Any],
        model_params: Dict[str, Any],
        progress_callback: Optional[Callable[[str], None]] = None
    ) -> TopicResult:
        """
        Execute full processing pipeline.
        
        Args:
            texts: List of documents
            preprocessing_options: {'remove_stopwords': bool, 'min_frequency': int, ...}
            model_params: Algorithm-specific parameters
            progress_callback: Optional function(progress_string) called during training
        
        Returns:
            TopicResult
        
        Example:
            processor = TopicProcessor(BERTopicAlgorithm())
            result = processor.process(
                texts=documents,
                preprocessing_options={'remove_stopwords': True},
                model_params={'min_topic_size': 5},
                progress_callback=lambda s: print(f"Progress: {s}")
            )
        """
        pass
```

---

### Exporter

**Location:** `models/services/exporter.py`

Export results to various formats.

```python
class Exporter:
    """Export results to CSV, JSON, etc."""
    
    def to_csv(
        self,
        result: TopicResult,
        output_path: str
    ) -> str:
        """
        Export results to CSV format.
        
        Args:
            result: TopicResult
            output_path: Path where to save CSV
        
        Returns:
            Path to saved file
        """
        pass
    
    def to_json(
        self,
        result: TopicResult,
        output_path: str
    ) -> str:
        """
        Export results to JSON format.
        
        Args:
            result: TopicResult
            output_path: Path where to save JSON
        
        Returns:
            Path to saved file
        """
        pass
```

---

### Visualizer

**Location:** `models/services/visualizer.py`

Generate visualizations for export to browser.

```python
class TopicVisualizer:
    """Generate visualizations to export as HTML"""
    
    def __init__(self, output_dir: Optional[str] = None):
        """
        Args:
            output_dir: Directory to save HTML files (default: ~/.bertopic-gui/viz)
        """
        pass
    
    def visualize(
        self,
        result: TopicResult,
        algorithm_name: str
    ) -> Dict[str, str]:
        """
        Generate visualizations for algorithm.
        
        Args:
            result: TopicResult
            algorithm_name: "BERTopic", "LDA", etc.
        
        Returns:
            Dict mapping viz_type → file_path
            Example:
            {
                'topics': '/home/user/.bertopic-gui/viz/topics.html',
                'documents': '/home/user/.bertopic-gui/viz/documents.html',
                'heatmap': '/home/user/.bertopic-gui/viz/heatmap.html'
            }
        """
        pass
    
    def open_visualization(self, file_path: str) -> None:
        """
        Open visualization in default browser.
        
        Args:
            file_path: Path to HTML file
        """
        pass
```

---

## Controllers

### AppController

**Location:** `controllers/app_controller.py`

Main event handler.

```python
class AppController:
    """Handle user interactions (file selection, algorithm changes, etc.)"""
    
    def __init__(self, app_state: AppState):
        """
        Args:
            app_state: AppState instance
        """
        pass
    
    def on_file_selected(self, file_path: str) -> None:
        """
        Handle file selection.
        Updates AppState, notifies views.
        
        Args:
            file_path: Path to selected file
        """
        pass
    
    def on_algorithm_changed(self, algorithm_name: str) -> None:
        """
        Handle algorithm selection change.
        Resets parameters to defaults.
        Updates AppState, notifies views.
        
        Args:
            algorithm_name: "BERTopic", "LDA", etc.
        """
        pass
    
    def on_param_changed(self, param_name: str, value: Any) -> None:
        """
        Handle parameter adjustment.
        Updates AppState, notifies views.
        
        Args:
            param_name: Parameter name
            value: New value
        """
        pass
```

---

### AnalysisController

**Location:** `controllers/analysis_controller.py`

Training pipeline orchestration.

```python
class AnalysisController:
    """Handle model training workflow"""
    
    def __init__(self, app_state: AppState):
        """
        Args:
            app_state: AppState instance
        """
        pass
    
    def run_analysis(self) -> None:
        """
        Execute analysis in background thread.
        Updates AppState with progress, results, errors.
        Calls state.notify() on updates.
        
        Flow:
        1. Validate inputs
        2. Load data
        3. Train model (with progress updates)
        4. Export visualizations
        5. Update AppState with result
        6. Handle errors gracefully
        """
        pass
```

---

## Views

### InputPanel

**Location:** `views/panels/input_panel.py`

File upload interface.

```python
class InputPanel(ttk.Frame):
    """File selection and preview"""
    
    def __init__(
        self,
        parent,
        app_state: AppState,
        controller: AppController
    ):
        """
        Args:
            parent: Parent ttkbootstrap widget
            app_state: AppState instance
            controller: AppController instance
        """
        pass
    
    def _on_state_changed(self, state: AppState) -> None:
        """
        Called by AppState.notify() when state changes.
        Re-render based on new state.
        
        Args:
            state: New AppState
        """
        pass
```

---

### SettingsPanel

**Location:** `views/panels/settings_panel.py`

Algorithm selection and parameter configuration.

```python
class SettingsPanel(ttk.Frame):
    """Algorithm and parameter controls"""
    
    def __init__(
        self,
        parent,
        app_state: AppState,
        controller: AppController
    ):
        """
        Args:
            parent: Parent ttkbootstrap widget
            app_state: AppState instance
            controller: AppController instance
        """
        pass
    
    def _on_state_changed(self, state: AppState) -> None:
        """
        Called when AppState changes.
        Re-generate parameter form if algorithm changed.
        
        Args:
            state: New AppState
        """
        pass
    
    def _build_parameter_form(self, param_schema: Dict) -> None:
        """
        Generate parameter form from schema.
        Creates widgets for int, float, choice, etc.
        
        Args:
            param_schema: From algorithm.get_param_schema()
        """
        pass
```

---

### ProcessingPanel

**Location:** `views/panels/processing_panel.py`

Training progress display.

```python
class ProcessingPanel(ttk.Frame):
    """Progress bar and status messages"""
    
    def __init__(
        self,
        parent,
        app_state: AppState,
        controller: AnalysisController
    ):
        """
        Args:
            parent: Parent ttkbootstrap widget
            app_state: AppState instance
            controller: AnalysisController instance
        """
        pass
    
    def _on_state_changed(self, state: AppState) -> None:
        """
        Called when AppState changes.
        Update progress bar, status text.
        
        Args:
            state: New AppState
        """
        pass
```

---

### ResultsPanel

**Location:** `views/panels/results_panel.py`

Results display and actions.

```python
class ResultsPanel(ttk.Frame):
    """Results display: topics, stats, action buttons"""
    
    def __init__(
        self,
        parent,
        app_state: AppState,
        controller: AppController
    ):
        """
        Args:
            parent: Parent ttkbootstrap widget
            app_state: AppState instance
            controller: AppController instance
        """
        pass
    
    def _on_state_changed(self, state: AppState) -> None:
        """
        Called when AppState changes.
        Display results if analysis complete.
        
        Args:
            state: New AppState
        """
        pass
    
    def _render_topics(self, result: TopicResult) -> None:
        """
        Display topic table.
        
        Args:
            result: TopicResult
        """
        pass
    
    def _render_stats(self, result: TopicResult) -> None:
        """
        Display metric cards (topic count, quality, etc.).
        
        Args:
            result: TopicResult
        """
        pass
```

---

## Example: Implementing a New Algorithm (LDA)

To add LDA support:

1. **Create** `models/algorithms/lda.py`:

```python
from models.algorithms.base_algorithm import BaseAlgorithm
from models.topic_result import TopicResult
from gensim.corpora import Dictionary
from gensim.models import LdaMulticore

class LDAAlgorithm(BaseAlgorithm):
    def train(self, texts, **params) -> TopicResult:
        # Tokenize
        dictionary = Dictionary([doc.split() for doc in texts])
        corpus = [dictionary.doc2bow(doc.split()) for doc in texts]
        
        # Train
        model = LdaMulticore(
            corpus=corpus,
            num_topics=params['num_topics'],
            id2word=dictionary,
            workers=params['workers'],
            passes=params['passes']
        )
        
        # Convert to standard format
        return TopicResult(
            topics=...,
            doc_topics=...,
            metadata={'model': model, 'dictionary': dictionary},
            model_info={'algorithm': 'LDA', ...}
        )
    
    def get_default_params(self):
        return {
            'num_topics': 10,
            'workers': 4,
            'passes': 10
        }
    
    def get_param_schema(self):
        return {
            'num_topics': {
                'type': 'int',
                'min': 2,
                'max': 100,
                'default': 10,
                'tooltip': 'Number of topics'
            },
            'workers': {
                'type': 'int',
                'min': 1,
                'max': 8,
                'default': 4,
                'tooltip': 'Number of worker processes'
            },
            'passes': {
                'type': 'int',
                'min': 1,
                'max': 100,
                'default': 10,
                'tooltip': 'Number of training passes'
            }
        }
    
    @property
    def algorithm_name(self):
        return "LDA (Gensim)"
```

2. **Update** `models/algorithms/__init__.py`:

```python
from .lda import LDAAlgorithm

AVAILABLE_ALGORITHMS = {
    'BERTopic': BERTopicAlgorithm,
    'LDA': LDAAlgorithm,  # NEW
}
```

3. **No UI changes needed!** Parameter form auto-generates from schema.

---

## Summary

- **TopicResult**: Standardized algorithm output
- **AppState**: Single source of truth
- **BaseAlgorithm**: Algorithm interface
- **Services**: DataLoader, Processor, Exporter, Visualizer
- **Controllers**: Handle user events, update AppState
- **Views**: Read AppState, call controller methods
- **Extending**: Add new algorithm by implementing BaseAlgorithm + updating registry
