"""Topic quality metrics for the Metrics tab.

Coherence metrics (UMass, C_V, NPMI) come from Gensim's ``CoherenceModel``;
Topic Diversity is implemented here because Gensim does not provide it
(decision D-020).
"""

from typing import Dict, List, Optional

from gensim.corpora.dictionary import Dictionary
from gensim.models.coherencemodel import CoherenceModel


def topic_diversity(topics: List[List[str]], top_n: int = 10) -> float:
    """Proportion of unique words across all topics' top-N words.

    diversity = |unique words| / (num_topics * top_n), in [0, 1].
    Higher means more distinct topics.
    """
    if not topics or top_n <= 0:
        return 0.0
    words = [word for topic in topics for word in topic[:top_n]]
    if not words:
        return 0.0
    return len(set(words)) / len(words)


def compute_topic_quality(
    topics: List[Dict[str, float]],
    texts: List[str],
    top_n: int = 10,
) -> Optional[Dict[str, Optional[float]]]:
    """Compute NPMI, C_V, UMass coherence and Topic Diversity.

    Returns a dict with keys ``npmi``, ``c_v``, ``u_mass``, ``topic_diversity``.
    A measure that cannot be computed (e.g. corpus too small) is ``None`` so the
    UI can show "N/A". Returns ``None`` if there are no topics or no texts to
    evaluate.
    """
    if not topics or not texts:
        return None

    # Extract top-N words per topic. Topic dicts are term->weight, ordered by
    # descending weight (BERTopic returns them sorted).
    topic_words: List[List[str]] = [list(t.keys())[:top_n] for t in topics]

    # Tokenize the training texts. They are already preprocessed and
    # lower-cased by TopicProcessor._preprocess.
    tokenized = [t.split() for t in texts if t.strip()]
    if not tokenized:
        return None

    metrics: Dict[str, Optional[float]] = {
        "npmi": None,
        "c_v": None,
        "u_mass": None,
        "topic_diversity": topic_diversity(topic_words, top_n),
    }

    # Gensim needs a BoW corpus + dictionary for the coherence measures.
    dictionary = Dictionary(tokenized)
    corpus = [dictionary.doc2bow(t) for t in tokenized]

    for measure, key in (("u_mass", "u_mass"), ("c_v", "c_v"), ("c_npmi", "npmi")):
        try:
            cm = CoherenceModel(
                topics=topic_words,
                texts=tokenized,
                corpus=corpus,
                dictionary=dictionary,
                coherence=measure,
                topn=top_n,
                # Single-process: Gensim's default multiprocessing for c_v /
                # c_npmi fails from a GUI app's background thread on macOS
                # spawn. processes=1 is reliable and fast for research corpora.
                processes=1,
            )
            metrics[key] = float(cm.get_coherence())
        except Exception:
            # A failed measure (e.g. corpus too small) leaves the value None;
            # the UI can show "N/A" instead of crashing the pipeline.
            metrics[key] = None

    return metrics
