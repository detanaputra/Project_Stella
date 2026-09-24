"""Tests for BERTopicAlgorithm (train, merge, delete, save/load)."""

import os

import pytest

from app.models.algorithms.bertopic import BERTopicAlgorithm


def _topic_ids(result):
    """The real (non-outlier) topic ids present in the result's doc assignments."""
    return sorted({tid for doc in result.doc_topics for tid in doc if tid != -1})


def test_train_shape(trained_result):
    result = trained_result
    assert len(result.topics) >= 1
    assert len(result.doc_topics) == len(result.metadata["texts"])
    assert "num_topics" in result.model_info
    assert result.metadata["model"] is not None
    assert all(isinstance(t, dict) for t in result.topics)


def test_merge_topics(fresh_result):
    result = fresh_result
    topic_ids = _topic_ids(result)
    if len(topic_ids) < 2:
        pytest.skip("need at least 2 topics to merge")
    algo = BERTopicAlgorithm()
    merged = algo.merge_topics(result, topic_ids[:2])
    assert len(merged.topics) < len(result.topics)
    assert len(merged.doc_topics) == len(result.doc_topics)


def test_delete_topics(fresh_result):
    result = fresh_result
    topic_ids = _topic_ids(result)
    if not topic_ids:
        pytest.skip("no topics to delete")
    algo = BERTopicAlgorithm()
    deleted = algo.delete_topics(result, [topic_ids[0]])
    assert len(deleted.topics) < len(result.topics)
    assert len(deleted.doc_topics) == len(result.doc_topics)


def test_model_id_generated(trained_result):
    assert trained_result.model_id is not None
    assert len(trained_result.model_id) > 0


def test_merge_preserves_model_id(fresh_result):
    result = fresh_result
    topic_ids = _topic_ids(result)
    if len(topic_ids) < 2:
        pytest.skip("need at least 2 topics to merge")
    merged = BERTopicAlgorithm().merge_topics(result, topic_ids[:2])
    assert merged.model_id == result.model_id


def test_save_load_round_trip(tmp_path, fresh_result):
    """The persistence feasibility check: save a model, load it, compare topics."""
    algo = BERTopicAlgorithm()
    model = fresh_result.metadata["model"]
    path = str(tmp_path / "model")
    algo.save_model(model, path)
    assert os.path.exists(path)
    loaded = algo.load_model(path)
    assert loaded is not None
    orig = model.get_topics()
    loaded_topics = loaded.get_topics()
    assert set(orig.keys()) == set(loaded_topics.keys())
    for tid in orig:
        assert [w for w, _ in orig[tid][:3]] == [w for w, _ in loaded_topics[tid][:3]]
