"""Tests for BERTopicAlgorithm (train, merge, delete)."""

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
