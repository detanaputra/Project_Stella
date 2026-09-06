"""Tests for AppController (file selection, algorithm change)."""

import os

from app.controllers.app_controller import AppController
from app.models.app_state import AppState

FIXTURES = os.path.join(os.path.dirname(__file__), "..", "fixtures")


def _path(name):
    return os.path.join(FIXTURES, name)


def test_on_file_selected():
    state = AppState()
    controller = AppController(state)
    controller.on_file_selected(_path("sample_data.csv"))
    assert state.selected_file_path == _path("sample_data.csv")
    assert len(state.file_preview) > 0


def test_on_file_selected_invalid():
    state = AppState()
    controller = AppController(state)
    controller.on_file_selected("/nonexistent/file.csv")
    assert state.analysis_error is not None


def test_on_algorithm_changed():
    state = AppState()
    controller = AppController(state)
    controller.on_algorithm_changed("BERTopic")
    assert state.selected_algorithm == "BERTopic"
    assert "bertopic_min_topic_size" in state.algorithm_params


def test_on_algorithm_changed_unknown():
    state = AppState()
    controller = AppController(state)
    controller.on_algorithm_changed("LDA")
    assert state.analysis_error is not None
