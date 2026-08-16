import numpy as np
from typing import List, Dict, Any
from bertopic import BERTopic
import bertopic
from hdbscan import HDBSCAN
from umap import UMAP
from bertopic.vectorizers import ClassTfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from app.models.algorithms.base_algorithm import BaseAlgorithm
from app.models.topic_result import TopicResult
import traceback

class BERTopicAlgorithm(BaseAlgorithm):
    """BERTopic implementation of the BaseAlgorithm interface"""

    @property
    def algorithm_name(self) -> str:
        return "BERTopic"

    def get_default_params(self) -> Dict[str, Any]:
        return {
            'bertopic_min_topic_size': 10,
            'bertopic_embedding_model': 'all-MiniLM-L6-v2',
            'bertopic_calculate_probabilities': True,
            'umap_n_neighbors': 15,
            'umap_n_components': 5,
            'umap_metric': 'cosine',
            'umap_low_memory': False,
            'hdbscan_min_samples': 10,
            'hdbscan_metric': 'euclidean'
        }

    def get_param_schema(self) -> Dict[str, Dict[str, Any]]:
        # This is kept for general algorithm compatibility, but BERTopic now uses modular sections
        return {
            'bertopic_min_topic_size': {
                'type': 'int',
                'min': 2,
                'max': 100,
                'default': 10,
                'tooltip': 'Minimum number of documents per topic'
            },
            'bertopic_embedding_model': {
                'type': 'choice',
                'options': ['all-MiniLM-L6-v2', 'paraphrase-MiniLM-L6-v2', 'all-mpnet-base-v2'],
                'default': 'all-MiniLM-L6-v2',
                'tooltip': 'Sentence-transformer model for embeddings'
            }
        }

    def train(self, texts: List[str], **params) -> TopicResult:
        """
        Train BERTopic model and return a standardized TopicResult.
        """
        try:
            # 1. Configure UMAP
            umap_model = UMAP(
                n_neighbors=int(params.get('umap_n_neighbors', 15)),
                n_components=int(params.get('umap_n_components', 5)),
                metric=params.get('umap_metric', 'cosine'),
                low_memory=bool(params.get('umap_low_memory', False)),
                random_state=8
            )

            # 2. Configure HDBSCAN
            clusterer = HDBSCAN(
                min_samples=int(params.get('hdbscan_min_samples', 10)),
                metric=params.get('hdbscan_metric', 'euclidean'),
                prediction_data=True
            )

            # 3. Configure Vectorizer and CT-IDF
            vectorizer = CountVectorizer(stop_words="english")
            ctfidf_model = ClassTfidfTransformer(bm25_weighting=True, reduce_frequent_words=True)

            # 4. Initialize BERTopic
            model = BERTopic(
                min_topic_size=int(params.get('bertopic_min_topic_size', 10)),
                embedding_model=params.get('bertopic_embedding_model', 'all-MiniLM-L6-v2'),
                calculate_probabilities=bool(params.get('bertopic_calculate_probabilities', True)),
                umap_model=umap_model,
                hdbscan_model=clusterer,
                vectorizer_model=vectorizer,
                ctfidf_model=ctfidf_model
            )

            # Fit the model
            topics, probs = model.fit_transform(texts)

            # 1. Extract Topics (term -> weight)
            # BERTopic stores topics as (word, weight) tuples in get_topic()
            topics_list = []
            # Topic -1 is outliers, we usually exclude it from the top topics list
            # here we substract - 1 because topic id always start with - 1, thus the usable topic id is len - 1
            for topic_id in range(len(model.get_topics().keys())-1):
                if topic_id == -1: continue

                topic_data = model.get_topic(topic_id)
                # Convert [(word, weight), ...] to {word: weight, ...}
                topics_list.append({word: weight for word, weight in topic_data})

            # 2. Extract Doc-Topic assignments
            # If calculate_probabilities=True, probs is a numpy array [n_docs, n_topics]
            doc_topics = []
            if isinstance(probs, np.ndarray):
                # Ensure probs is 2D even if only one topic was found
                if probs.ndim == 1:
                    probs = probs.reshape(-1, 1)

                # Map each doc to a dict of {topic_id: probability}
                # BERTopic's probs array corresponds to the topics in model.get_topics()
                # Topic -1 is not usually in the probs array
                topic_names = list(model.get_topics().keys())
                # Filter out -1 for probability mapping
                filtered_topics = [t for t in topic_names if t != -1]

                for doc_prob in probs:
                    # Map prob index to actual topic_id
                    doc_map = {filtered_topics[i]: prob for i, prob in enumerate(doc_prob)}
                    doc_topics.append(doc_map)
            else:
                # Fallback to hard assignment
                for t in topics:
                    doc_topics.append({t: 1.0})

            # 3. Metadata & Model Info
            metadata = {
                'model': model,
                'texts': texts,
                'num_topics': len(model.get_topics()) - 1 # exclude -1
            }

            model_info = {
                'algorithm': self.algorithm_name,
                'version': bertopic.__version__,
                'params': str(params),
                'num_documents': str(len(texts)),
                'num_topics': str(len(model.get_topics()) - 1)
            }

            return TopicResult(
                topics=topics_list,
                doc_topics=doc_topics,
                metadata=metadata,
                model_info=model_info
            )

        except Exception as e:
            call_stack = traceback.format_exc()
            raise RuntimeError(f"BERTopic training failed: {str(e)}\n\n {call_stack}") from e
