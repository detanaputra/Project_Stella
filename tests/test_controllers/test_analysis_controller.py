"""Tests for AnalysisController (training pipeline)."""

import os
import time

from app.controllers.analysis_controller import AnalysisController
from app.models.app_state import AppState

FIXTURES = os.path.join(os.path.dirname(__file__), "..", "fixtures")


def _path(name):
    return os.path.join(FIXTURES, name)


def test_run_analysis_no_file():
    state = AppState()
    controller = AnalysisController(state)
    controller.run_analysis()
    assert state.analysis_error is not None


def test_run_analysis_reentrancy():
    state = AppState()
    state.selected_file_path = _path("sample_data.csv")
    state.analysis_in_progress = True
    controller = AnalysisController(state)
    controller.run_analysis()  # guard returns early while a run is in progress
    assert state.analysis_in_progress is True


def test_run_analysis_full_pipeline():
    state = AppState()
    state.selected_file_path = _path("sample_data.csv")
    controller = AnalysisController(state)
    controller.run_analysis()
    deadline = time.time() + 120
    while state.analysis_in_progress and time.time() < deadline:
        time.sleep(0.2)
    assert state.analysis_in_progress is False
    assert state.current_result is not None
