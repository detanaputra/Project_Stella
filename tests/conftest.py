"""Shared pytest fixtures for the Stella test suite (v0.5.0, WP1)."""

import pytest

from app.models.app_state import AppState
from app.models.algorithms.bertopic import BERTopicAlgorithm


# A small, clearly-separated corpus so BERTopic forms topics reliably and fast.
SAMPLE_TEXTS = [
    # climate (10)
    "climate change is warming the planet",
    "carbon emissions are rising every year",
    "renewable energy can replace fossil fuels",
    "the polar ice caps are melting rapidly",
    "sea levels are rising due to global warming",
    "solar and wind power are clean energy sources",
    "governments must cut greenhouse gas emissions",
    "deforestation accelerates climate change",
    "the paris agreement targets net zero emissions",
    "extreme weather events are becoming more frequent",
    # sports (10)
    "the football team won the championship",
    "the basketball player scored forty points",
    "tennis requires agility and endurance",
    "the marathon runner finished in record time",
    "swimming is a great full body workout",
    "the coach trained the players every morning",
    "the olympics bring athletes from around the world",
    "cricket is popular in many countries",
    "the goalkeeper made an incredible save",
    "cycling up the mountain was exhausting",
    # technology (10)
    "artificial intelligence is transforming industries",
    "the new smartphone has a better camera",
    "software developers write code every day",
    "cloud computing stores data remotely",
    "machine learning models predict outcomes",
    "the internet connects billions of people",
    "robots are automating factory work",
    "cybersecurity protects against hackers",
    "virtual reality creates immersive experiences",
    "the startup launched a new mobile app",
    # food (10)
    "pizza is a popular italian dish",
    "fresh vegetables make a healthy salad",
    "the chef prepared a gourmet dinner",
    "chocolate is made from cocoa beans",
    "baking bread requires flour and yeast",
    "sushi is a traditional japanese food",
    "coffee is brewed from roasted beans",
    "the restaurant serves delicious pasta",
    "fruits are full of vitamins",
    "cooking at home saves money",
]


def _train():
    """Train a BERTopicAlgorithm on the small corpus with a low min_topic_size
    so topics form reliably on a tiny dataset. nr_topics=None avoids BERTopic's
    auto-reduction, which re-clusters the outlier docs and crashes when there
    are none (a latent edge case in the app's 'auto' default)."""
    algo = BERTopicAlgorithm()
    params = algo.get_default_params()
    params["bertopic_min_topic_size"] = 2
    params["bertopic_nr_topics"] = None
    # The app's HDBSCAN defaults (min_cluster_size=10) cluster a 40-doc corpus
    # into noise; lower them so topics form reliably on the tiny test corpus.
    params["hdbscan_min_cluster_size"] = 2
    params["hdbscan_min_samples"] = 2
    return algo.train(SAMPLE_TEXTS, **params)


@pytest.fixture(scope="session")
def sample_texts():
    return list(SAMPLE_TEXTS)


@pytest.fixture(scope="session")
def trained_result():
    """A trained TopicResult, reused by read-only tests (trained once per session)."""
    return _train()


@pytest.fixture
def fresh_result():
    """A freshly trained TopicResult per test — for tests that mutate the model
    (merge/delete), so one test's mutation cannot leak into another."""
    return _train()


@pytest.fixture
def app_state():
    return AppState()
