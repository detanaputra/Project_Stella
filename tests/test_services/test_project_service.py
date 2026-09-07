"""Tests for ProjectService (zip-bundle save/load, v0.5.0 WP3).

A ``.stella`` file is a zip archive holding project.json (state + full result
data) plus model/{model_id}/ and viz/{model_id}/. Load restores the result
including the trained model.
"""

import json
import os
import zipfile

from app.models.app_state import AppState
from app.models.services.project_service import ProjectService

FIXTURES = os.path.join(os.path.dirname(__file__), "..", "fixtures")


def _path(name):
    return os.path.join(FIXTURES, name)


def test_save_project_creates_zip(tmp_path, trained_result):
    state = AppState()
    state.current_result = trained_result
    state.selected_file_path = _path("sample_data.csv")
    out = os.path.join(tmp_path, "project.stella")
    ProjectService().save_project(state, out)
    assert os.path.exists(out)
    with zipfile.ZipFile(out) as zf:
        names = zf.namelist()
        assert "project.json" in names
        data = json.loads(zf.read("project.json").decode("utf-8"))
    assert data["selected_file_path"] == _path("sample_data.csv")
    models = data["models"]
    assert trained_result.model_id in models
    assert models[trained_result.model_id]["selected_algorithm"] == "BERTopic"
    assert models[trained_result.model_id]["result"]["model_id"] == trained_result.model_id


def test_save_load_round_trip(tmp_path, trained_result, monkeypatch):
    monkeypatch.setattr(ProjectService, "STELLA_DIR", str(tmp_path / "stella"))

    state = AppState()
    state.current_result = trained_result
    state.selected_file_path = _path("sample_data.csv")
    out = os.path.join(tmp_path, "project.stella")
    ProjectService().save_project(state, out)

    state2 = AppState()
    ProjectService().load_project(out, state2)
    assert state2.current_result is not None
    loaded = state2.current_result
    assert loaded.model_id == trained_result.model_id
    assert loaded.topics == trained_result.topics
    assert loaded.doc_topics == trained_result.doc_topics
    assert loaded.model_info == trained_result.model_info
    assert loaded.metadata["model"] is not None  # the trained model is restored
    assert loaded.metadata["texts"] == trained_result.metadata["texts"]


def test_load_project_restores_state(tmp_path, monkeypatch):
    monkeypatch.setattr(ProjectService, "STELLA_DIR", str(tmp_path / "stella"))
    project = {
        "selected_file_path": _path("sample_data.csv"),
        "models": {
            "20260907-000000": {
                "selected_algorithm": "BERTopic",
                "algorithm_params": {"bertopic_min_topic_size": 5},
                "result": None,
            }
        },
    }
    path = os.path.join(tmp_path, "project.stella")
    with zipfile.ZipFile(path, "w") as zf:
        zf.writestr("project.json", json.dumps(project))
    state = AppState()
    ProjectService().load_project(path, state)
    assert state.selected_algorithm == "BERTopic"
    assert state.algorithm_params["bertopic_min_topic_size"] == 5
    assert state.current_result is None  # no result data -> no result rebuilt
