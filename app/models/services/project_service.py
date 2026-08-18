import json
import os
from typing import Any, Dict
from app.models.app_state import AppState
from app.models.algorithms import AVAILABLE_ALGORITHMS, get_algorithm

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

        # Validate the algorithm name: a stale/altered .stella must not put the
        # app into a state that crashes at train time (audit L7).
        algo = data.get("selected_algorithm", "BERTopic")
        if algo not in AVAILABLE_ALGORITHMS:
            algo = "BERTopic"
        state.selected_algorithm = algo

        # Guard against missing/corrupt params, and merge any loaded values
        # over the algorithm's defaults so a partial/older .stella still
        # trains with a complete, valid parameter set (audit L7).
        loaded = data.get("algorithm_params")
        if not isinstance(loaded, dict):
            loaded = {}
        state.algorithm_params = {**get_algorithm(algo).get_default_params(), **loaded}

        # A recorded data path that no longer exists would fail at train time
        # with a confusing error; clear it so the UI prompts for a new file.
        file_path = data.get("selected_file_path")
        if file_path and not os.path.exists(file_path):
            file_path = None
        state.selected_file_path = file_path

        # We can't restore the model object from JSON, so we reset current_result
        state.current_result = None
