from typing import Dict, Type
from .base_algorithm import BaseAlgorithm
from .bertopic import BERTopicAlgorithm

AVAILABLE_ALGORITHMS: Dict[str, Type[BaseAlgorithm]] = {
    'BERTopic': BERTopicAlgorithm,
}

def get_algorithm(name: str) -> BaseAlgorithm:
    """Factory function to get an instance of the requested algorithm."""
    if name not in AVAILABLE_ALGORITHMS:
        raise ValueError(f"Unknown algorithm: {name}")
    return AVAILABLE_ALGORITHMS[name]()
