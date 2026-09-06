from dataclasses import dataclass
from typing import List, Dict, Any, Optional

@dataclass
class TopicResult:
    """Standardized topic modelling output across all algorithms"""

    topics: List[Dict[str, float]]
    """
    List of topics. Each topic is a dict mapping term -> weight.
    Example: [{"climate": 0.12, "environmental": 0.11, "carbon": 0.10, ...}, ...]
    """

    doc_topics: List[Dict[int, float]]
    """
    List of document-topic assignments.
    Each document maps topic_id -> probability.
    Example: [{0: 0.85, 2: 0.15}, {1: 0.70, 3: 0.30}, ...]
    """

    metadata: Dict[str, Any]
    """
    Algorithm-specific metadata.
    Example: {'model': <BERTopic instance>, 'texts': [list of input texts], ...}
    """

    model_info: Dict[str, str]
    """
    Algorithm info for reproducibility.
    Example: {'algorithm': 'BERTopic', 'version': '0.15.0', 'num_topics': '12'}
    """

    quality_metrics: Optional[Dict[str, float]] = None
    """
    Topic quality evaluation, computed by the pipeline after training (not by the
    algorithm itself). One value per metric, averaged across topics.
    Example: {'npmi': 0.12, 'c_v': 0.45, 'u_mass': -3.2, 'topic_diversity': 0.78}
    """

    topic_labels: Optional[Dict[int, str]] = None
    """
    User-provided names/interpretations per topic, set via topic refinement
    (v0.4.0, WP1). Maps topic_id -> label; shown in the topics table.
    """
