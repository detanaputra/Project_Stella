"""Tests for DataLoader (file validation, preview, text loading)."""

import os

from app.models.services.data_loader import DataLoader

FIXTURES = os.path.join(os.path.dirname(__file__), "..", "fixtures")


def _path(name):
    return os.path.join(FIXTURES, name)


def test_validate_file_missing():
    result = DataLoader().validate_file("/nonexistent/file.csv")
    assert result.is_valid is False
    assert result.error


def test_validate_file_wrong_format():
    result = DataLoader().validate_file(_path("notes.md"))
    assert result.is_valid is False
    assert "format" in result.error.lower()


def test_validate_file_valid_csv():
    result = DataLoader().validate_file(_path("sample_data.csv"))
    assert result.is_valid is True


def test_load_texts_csv():
    texts = DataLoader().load_texts(_path("sample_data.csv"))
    assert len(texts) > 0
    assert all(isinstance(t, str) and t.strip() for t in texts)


def test_load_preview_csv():
    preview = DataLoader().load_preview(_path("sample_data.csv"), n_lines=3)
    assert len(preview) == 3


def test_load_texts_txt():
    texts = DataLoader().load_texts(_path("sample_data.txt"))
    assert len(texts) > 0
