"""Tests for Exporter (CSV topics/assignments, JSON record, methodology report)."""

import json
import os

from app.models.app_state import AppState
from app.models.services.exporter import Exporter


def _state_with_result(result):
    state = AppState()
    state.current_result = result
    return state


def test_to_json_models_dict(tmp_path, trained_result):
    out = os.path.join(tmp_path, "result.json")
    Exporter().to_json(_state_with_result(trained_result), out)
    with open(out) as f:
        data = json.load(f)
    assert "models" in data
    models = data["models"]
    assert trained_result.model_id in models
    entry = models[trained_result.model_id]
    assert entry["selected_algorithm"] == "BERTopic"
    assert "topics" in entry["result"]
    assert "doc_topics" in entry["result"]
    assert "texts" not in entry["result"]  # input data excluded from the record
    assert "original_texts" not in entry["result"]


def test_to_csv_topics(tmp_path, trained_result):
    out = os.path.join(tmp_path, "topics.csv")
    Exporter().to_csv_topics(_state_with_result(trained_result), out)
    with open(out) as f:
        content = f.read()
    assert "Model ID" in content
    assert "Topic ID" in content
    assert "Word 1" in content


def test_to_csv_assignments(tmp_path, trained_result):
    out = os.path.join(tmp_path, "assignments.csv")
    Exporter().to_csv_assignments(_state_with_result(trained_result), out)
    with open(out) as f:
        content = f.read()
    assert "Model ID" in content
    assert "Doc Index" in content
    assert "Topic 1" in content


def test_generate_methodology_report(tmp_path, trained_result):
    out = os.path.join(tmp_path, "report.md")
    Exporter().generate_methodology_report(trained_result, out)
    with open(out) as f:
        content = f.read()
    assert "Topic Modelling Methodology Report" in content
