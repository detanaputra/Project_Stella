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
