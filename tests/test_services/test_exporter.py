"""Tests for Exporter (CSV, JSON, methodology report)."""

import json
import os

from app.models.services.exporter import Exporter


def test_to_csv(tmp_path, trained_result):
    out = os.path.join(tmp_path, "topics.csv")
    Exporter().to_csv(trained_result, out)
    assert os.path.exists(out)
    with open(out) as f:
        content = f.read()
    assert "topic" in content


def test_to_json(tmp_path, trained_result):
    out = os.path.join(tmp_path, "result.json")
    Exporter().to_json(trained_result, out)
    with open(out) as f:
        data = json.load(f)
    assert "topics" in data
    assert "doc_topics" in data
    assert "model_info" in data


def test_generate_methodology_report(tmp_path, trained_result):
    out = os.path.join(tmp_path, "report.md")
    Exporter().generate_methodology_report(trained_result, out)
    with open(out) as f:
        content = f.read()
    assert "Topic Modelling Methodology Report" in content
