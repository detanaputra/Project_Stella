import threading
from typing import Optional, Dict, Any
from app.models.app_state import AppState
from app.models.services.data_loader import DataLoader
from app.models.services.processor import TopicProcessor
from app.models.services.visualizer import TopicVisualizer
from app.models.services.exporter import Exporter
from app.models.algorithms import get_algorithm

class AnalysisController:
    """Handle the model training workflow in a background thread."""

    def __init__(self, state: AppState):
        self.appState: AppState = state
        self.loader = DataLoader()
        self.visualizer = TopicVisualizer()
        self.exporter = Exporter()

    def run_analysis(self) -> None:
        """Launch the analysis pipeline in a background thread to keep UI responsive."""
        if self.appState.analysis_in_progress:
            # Re-entrancy guard: prevent a second click from spawning another
            # training thread while one is already running (audit M1).
            return
        if not self.appState.selected_file_path:
            self.appState.analysis_error = "Please select a file first."
            self.appState.notify()
            return

        # Set synchronously so a rapid double-click is caught by the guard
        # above before the worker thread starts.
        self.appState.analysis_in_progress = True

        # Start training in background
        thread = threading.Thread(target=self._execute_pipeline, daemon=True)
        thread.start()

    def _execute_pipeline(self) -> None:
        """The background worker process."""
        try:
            # 1. Setup State
            self.appState.analysis_in_progress = True
            self.appState.analysis_error = None
            self.appState.analysis_progress = "0%"
            self.appState.analysis_status = "Initializing background thread..."
            self.appState.notify()

            # 2. Load Data
            self.appState.analysis_status = "Loading data from file..."
            self.appState.notify()
            texts = self.loader.load_texts(self.appState.selected_file_path)

            if not texts:
                raise ValueError("No text data found in the selected file.")

            # 3. Initialize Processor
            self.appState.analysis_status = "Initializing algorithm..."
            self.appState.notify()
            algo = get_algorithm(self.appState.selected_algorithm)
            processor = TopicProcessor(algo)

            # 4. Execute Training with progress updates
            def update_progress(status: str):
                self.appState.analysis_status = status
                self.appState.notify()

            # Preprocessing options
            preprocessing_options = {
                'remove_urls': True,
                'remove_numbers': True,
                'remove_emails': True,
                'custom_stopwords_path': None
            }

            self.appState.analysis_status = "Preprocessing and training model (this may take a few minutes)..."
            self.appState.notify()

            result = processor.process(
                texts=texts,
                preprocessing_options=preprocessing_options,
                model_params=self.appState.algorithm_params,
                progress_callback=update_progress
            )

            # 5. Finalize
            self.appState.current_result = result
            self.appState.analysis_in_progress = False
            self.appState.analysis_progress = "100%"
            self.appState.analysis_status = "Analysis complete!"
            self.appState.notify()

        except Exception as e:
            # Keep the traceback here: analysis_error only stores str(e), so
            # this stderr log is the sole record of a failed run for support.
            import traceback
            traceback.print_exc()
            self.appState.analysis_in_progress = False
            self.appState.analysis_error = f"Analysis failed: {str(e)}"
            self.appState.analysis_status = "Analysis failed"
            self.appState.notify()
