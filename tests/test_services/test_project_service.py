"""Tests for ProjectService (current lossy save/load behavior).

These lock in the current behavior: save writes only state + model_info, and
load resets current_result to None. They will be updated when the persistence
rework (v0.5.0 WP2/WP3) lands.
"""

import json
import os

from app.models.app_state import AppState
from app.models.services.project_service import ProjectService

FIXTURES = os.path.join(os.path.dirname(__file__), "..", "fixtures")


def _path(name):
    return os.path.join(FIXTURES, name)


def test_save_project(tmp_path, trained_result):
    state = AppState()
    state.current_result = trained_result
    state.selected_file_path = _path("sample_data.csv")
    out = os.path.join(tmp_path, "project.stella")
    ProjectService().save_project(state, out)
    with open(out) as f:
        data = json.load(f)
    assert data["selected_file_path"] == _path("sample_data.csv")
    assert data["selected_algorithm"] == "BERTopic"
    assert "result_metadata" in data


def test_load_project_resets_result(tmp_path):
    state = AppState()
    project = {
        "selected_file_path": _path("sample_data.csv"),
        "selected_algorithm": "BERTopic",
        "algorithm_params": {"bertopic_min_topic_size": 5},
    }
    path = os.path.join(tmp_path, "project.stella")
    with open(path, "w") as f:
        json.dump(project, f)
    ProjectService().load_project(path, state)
    assert state.selected_algorithm == "BERTopic"
    assert state.algorithm_params["bertopic_min_topic_size"] == 5
    assert state.current_result is None  # the model cannot be restored (current behavior)
