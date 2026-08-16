from typing import Any
from app.models.app_state import AppState
from app.models.services.data_loader import DataLoader
from app.models.services.project_service import ProjectService
from app.models.algorithms import get_algorithm

class AppController:
    """Handle user interactions for project setup, file selection, and project management."""

    def __init__(self, state: AppState):
        self.appState: AppState = state
        self.loader = DataLoader()
        self.project_service = ProjectService()

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
