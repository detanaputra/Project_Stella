from typing import List, Dict, Any, Optional, Callable
from app.models.algorithms.base_algorithm import BaseAlgorithm
from app.models.topic_result import TopicResult
import re

class TopicProcessor:
    """Orchestrate model training and preprocessing for social scientists."""

    def __init__(self, algorithm: BaseAlgorithm):
        self.algorithm = algorithm

    def _preprocess(self, texts: List[str], options: Dict[str, Any]) -> List[str]:
        """
        Apply noise filtering and stop-word removal.
        """
        processed_texts = []

        # Custom stop-words from file or list
        stop_words = set()
        if 'custom_stopwords_path' in options:
            path = options['custom_stopwords_path']
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    stop_words = {line.strip().lower() for line in f if line.strip()}
            except Exception:
                pass # Fallback to empty if file fails

        for text in texts:
            t = text.lower()

            # Noise Filtering
            if options.get('remove_urls', False):
                t = re.sub(r'http\S+|www\S+|https\S+', '', t, flags=re.MULTILINE)

            if options.get('remove_numbers', False):
                t = re.sub(r'\d+', '', t)

            if options.get('remove_emails', False):
                t = re.sub(r'\S+@\S+', '', t)

            # Stop-word removal
            if stop_words:
                words = t.split()
                t = " ".join([w for w in words if w not in stop_words])

            processed_texts.append(t.strip())

        return processed_texts

    def process(
        self,
        texts: List[str],
        preprocessing_options: Dict[str, Any],
        model_params: Dict[str, Any],
        progress_callback: Optional[Callable[[str], None]] = None
    ) -> TopicResult:
        """
        Execute full processing pipeline: Preprocess -> Train.
        """
        if progress_callback:
            progress_callback("Preprocessing text...")

        processed_texts = self._preprocess(texts, preprocessing_options)

        if progress_callback:
            progress_callback("Training model...")

        # The algorithm.train method handles the actual modelling
        result = self.algorithm.train(processed_texts, **model_params)

        if progress_callback:
            progress_callback("Training Done")

        return result
