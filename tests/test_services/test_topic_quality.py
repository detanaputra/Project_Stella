"""Tests for the topic quality service."""

from app.models.services.topic_quality import compute_topic_quality, topic_diversity


def test_topic_diversity_distinct():
    topics = [["a", "b", "c"], ["d", "e", "f"]]
    assert topic_diversity(topics, top_n=3) == 1.0


def test_topic_diversity_overlap():
    topics = [["a", "b", "c"], ["a", "b", "d"]]
    assert topic_diversity(topics, top_n=3) == 4 / 6


def test_compute_topic_quality_keys():
    topics = [{"a": 0.5, "b": 0.3, "c": 0.2}, {"d": 0.4, "e": 0.4, "f": 0.2}]
    texts = ["a b c", "d e f", "a b", "d e"]
    metrics = compute_topic_quality(topics, texts, top_n=3)
    assert metrics is not None
    assert "npmi" in metrics
    assert "c_v" in metrics
    assert "u_mass" in metrics
    assert "topic_diversity" in metrics


def test_compute_topic_quality_empty():
    assert compute_topic_quality([], ["a b"]) is None
    assert compute_topic_quality([{"a": 1.0}], []) is None
