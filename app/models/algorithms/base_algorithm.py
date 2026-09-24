from abc import ABC, abstractmethod
from typing import List, Dict, Any
from app.models.topic_result import TopicResult

class BaseAlgorithm(ABC):
    """Abstract interface all topic modelling algorithms must implement"""

    @abstractmethod
    def train(self, texts: List[str], **params) -> TopicResult:
        """
        Train the algorithm on texts.

        Args:
            texts: List of documents (strings)
            **params: Algorithm-specific parameters (from AppState.algorithm_params)

        Returns:
            TopicResult with standardized format

        Raises:
            ValueError: If parameters invalid
            RuntimeError: If training fails
        """
        pass

    @abstractmethod
    def get_default_params(self) -> Dict[str, Any]:
        """
        Get default parameters for this algorithm.

        Returns:
            Dict mapping param_name -> default_value
        """
        pass

    @abstractmethod
    def get_param_schema(self) -> Dict[str, Dict[str, Any]]:
        """
        Get parameter schema for UI form generation.

        Returns:
            Dict mapping param_name -> schema dict
            Schema dict structure:
                {
                    'type': 'int' | 'float' | 'choice' | 'range',
                    'min': number (for int/float),
                    'max': number (for int/float),
                    'default': value,
                    'options': [list] (for choice type),
                    'tooltip': 'Help text shown to user'
                }
        """
        pass

    @property
    @abstractmethod
    def algorithm_name(self) -> str:
        """
        Human-readable algorithm name.
        Returns: String like "BERTopic", "LDA", "NMF"
        """
        pass

    @abstractmethod
    def save_model(self, model, path: str) -> None:
        """
        Persist a trained model to a directory (path).

        The per-model directory (e.g. model/{model_id}/) is the unit; each
        algorithm writes its library's native serialization inside it.
        """
        pass

    @abstractmethod
    def load_model(self, path: str):
        """
        Load a trained model from a directory (path).
        """
        pass
