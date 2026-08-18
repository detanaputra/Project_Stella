from typing import Any, Optional
from app.models.app_state import AppState
from app.models.services.data_loader import DataLoader
from app.models.services.exporter import Exporter
from app.models.services.visualizer import TopicVisualizer
from app.models.services.project_service import ProjectService
from app.models.algorithms import get_algorithm

class AppController:
    """Handle user interactions for project setup, file selection, and project management."""

    def __init__(self, state: AppState):
        self.appState: AppState = state
        self.loader = DataLoader()
        self.exporter = Exporter()
        self.visualizer = TopicVisualizer()
        self.project_service = ProjectService()
        # Ensure the current algorithm's defaults are present from startup so
        # the main-window retrain path trains with the same parameters as the
        # wizard's "Default Settings" (audit H2/H6).
        if not state.algorithm_params:
            try:
                state.algorithm_params = get_algorithm(state.selected_algorithm).get_default_params()
            except Exception:
                pass  # leave empty; train() falls back to its own defaults

    def on_file_selected(self, file_path: str) -> None:
        """Handle file selection and update state with preview and guidance."""
        validation = self.loader.validate_file(file_path)

        if not validation.is_valid:
            self.appState.analysis_error = validation.error
            self.appState.notify()
            return

        # Update state
        self.appState.selected_file_path = file_path
        self.appState.file_preview = self.loader.load_preview(file_path)
        self.appState.analysis_error = None

        # Note: we could store validation.warnings in state if we have a UI for them
        self.appState.notify()

    def on_algorithm_changed(self, algorithm_name: str) -> None:
        """Handle algorithm switch and reset parameters."""
        try:
            algo = get_algorithm(algorithm_name)
            self.appState.selected_algorithm = algorithm_name
            self.appState.algorithm_params = algo.get_default_params()
            self.appState.notify()
        except ValueError as e:
            self.appState.analysis_error = str(e)
            self.appState.notify()

    def on_param_changed(self, param_name: str, value: Any) -> None:
        """Handle parameter adjustment."""
        self.appState.algorithm_params[param_name] = value
        self.appState.notify()

    def export_csv(self, output_path: str) -> None:
        """Export the current TopicResult to CSV."""
        if self.appState.current_result:
            self.exporter.to_csv(self.appState.current_result, output_path)

    def export_json(self, output_path: str) -> None:
        """Export the current TopicResult to JSON (audit M4)."""
        if self.appState.current_result:
            self.exporter.to_json(self.appState.current_result, output_path)

    def export_methodology_report(self, output_path: str) -> None:
        """Export the methodology report for the current TopicResult."""
        if self.appState.current_result:
            self.exporter.generate_methodology_report(self.appState.current_result, output_path)

    def export_visualizations(self) -> Optional[str]:
        """Generate offline HTML visualizations and open them in the browser.

        Returns an error message if nothing was exported, else None.
        Safe to call from a background thread; only touches the model and
        file system, never Tkinter (audit M1/M4).
        """
        if not self.appState.current_result:
            return "No analysis results to visualize."
        viz_files = self.visualizer.visualize(
            self.appState.current_result, self.appState.selected_algorithm
        )
        if not viz_files:
            return "No visualizations could be generated for this result."
        for path in viz_files.values():
            self.visualizer.open_visualization(path)
        return None

    def save_project(self, output_path: str) -> None:
        """Save current session to file."""
        try:
            self.project_service.save_project(self.appState, output_path)
        except Exception as e:
            self.appState.analysis_error = f"Save failed: {str(e)}"
            self.appState.notify()

    def load_project(self, input_path: str) -> None:
        """Load session from file."""
        try:
            self.project_service.load_project(input_path, self.appState)
            self.appState.notify()
        except Exception as e:
            self.appState.analysis_error = f"Load failed: {str(e)}"
            self.appState.notify()
