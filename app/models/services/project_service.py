import json
import os
from typing import Any, Dict
from app.models.app_state import AppState

class ProjectService:
    """Handle saving and loading of project state to .stella files."""

    def save_project(self, state: AppState, output_path: str) -> str:
        """
        Serialize the current AppState to a JSON file.
        """
        project_data = {
            "selected_file_path": state.selected_file_path,
            "selected_algorithm": state.selected_algorithm,
            "algorithm_params": state.algorithm_params,
            # We don't save the result itself (too large), but we save its metadata
            "result_metadata": state.current_result.model_info if state.current_result else None
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(project_data, f, indent=4)

        return output_path

    def load_project(self, input_path: str, state: AppState) -> None:
        """
        Deserialize a .stella file and update the AppState.
        """
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        state.selected_file_path = data.get("selected_file_path")
        state.selected_algorithm = data.get("selected_algorithm", "BERTopic")
        state.algorithm_params = data.get("algorithm_params", {})

        # We can't restore the model object from JSON, so we reset current_result
        state.current_result = None
