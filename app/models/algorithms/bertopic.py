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
        # Mirrors the defaults shown in the BERTopic/UMAP/HDBSCAN UI sections so
        # "Default Settings" (wizard) and the main-window retrain path agree.
        return {
            'bertopic_language': 'english',
            'bertopic_embedding_model': 'all-MiniLM-L6-v2',
            'bertopic_top_n_words': 10,
            'bertopic_ngram_range': (1, 2),
            'bertopic_min_topic_size': 10,
            'bertopic_nr_topics': 'auto',
            'bertopic_low_memory': False,
            'bertopic_calculate_probabilities': True,
            'umap_n_neighbors': 15,
            'umap_n_components': 5,
            'umap_metric': 'cosine',
            'umap_low_memory': False,
            'hdbscan_min_samples': 10,
            'hdbscan_min_cluster_size': 10,
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
            # min_cluster_size was missing entirely (audit M8); without it a
            # custom clusterer leaves BERTopic's clustering unconstrained.
            # Default it to the same value as min_topic_size for consistency.
            clusterer = HDBSCAN(
                min_samples=int(params.get('hdbscan_min_samples', 10)),
                min_cluster_size=int(params.get('hdbscan_min_cluster_size', 10)),
                metric=params.get('hdbscan_metric', 'euclidean'),
                prediction_data=True
            )

            # 3. Configure Vectorizer and CT-IDF.
            # Wire the language (stop-word selection) and n-gram range from the
            # UI so these hyperparameters actually take effect (audit H3).
            language = str(params.get('bertopic_language', 'english')).lower()
            stop_words = "english" if language == "english" else None

            if 'bertopic_ngram_range' in params and params['bertopic_ngram_range']:
                ngram_range = tuple(params['bertopic_ngram_range'])
            else:
                # Legacy individual keys written by older trace bindings
                ngram_range = (
                    int(params.get('bertopic_ngram_start', 1)),
                    int(params.get('bertopic_ngram_end', 2))
                )
            ngram_start, ngram_end = ngram_range
            if ngram_start > ngram_end:
                ngram_start, ngram_end = ngram_end, ngram_start  # guard invalid UI input

            vectorizer = CountVectorizer(stop_words=stop_words, ngram_range=(ngram_start, ngram_end))
            ctfidf_model = ClassTfidfTransformer(bm25_weighting=True, reduce_frequent_words=True)

            # 4. Initialize BERTopic
            # Normalize the UI's nr_topics ("auto", "None", or an int as a string)
            nr_topics = params.get('bertopic_nr_topics', 'auto')
            if isinstance(nr_topics, str):
                nr_topics_lower = nr_topics.strip().lower()
                if nr_topics_lower == 'none':
                    nr_topics = None
                elif nr_topics_lower != 'auto':
                    try:
                        nr_topics = int(nr_topics)
                    except (TypeError, ValueError):
                        nr_topics = None  # unrecognized input -> no reduction

            model = BERTopic(
                min_topic_size=int(params.get('bertopic_min_topic_size', 10)),
                embedding_model=params.get('bertopic_embedding_model', 'all-MiniLM-L6-v2'),
                calculate_probabilities=bool(params.get('bertopic_calculate_probabilities', True)),
                top_n_words=int(params.get('bertopic_top_n_words', 10)),
                nr_topics=nr_topics,
                low_memory=bool(params.get('bertopic_low_memory', False)),
                umap_model=umap_model,
                hdbscan_model=clusterer,
                vectorizer_model=vectorizer,
                ctfidf_model=ctfidf_model
            )

            # Fit the model
            topics, probs = model.fit_transform(texts)

            # 1. Extract Topics (term -> weight)
            # Topic -1 is the outliers topic; exclude it. Iterate the actual
            # topic ids rather than assuming they are contiguous integers, which
            # breaks once nr_topics reduction is used (audit H3 robustness).
            topic_ids = sorted(t for t in model.get_topics().keys() if t != -1)
            topics_list = []
            for topic_id in topic_ids:
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

                # BERTopic's probs array corresponds to the topics in model.get_topics()
                # Topic -1 is not usually in the probs array
                topic_names = list(model.get_topics().keys())
                filtered_topics = [t for t in topic_names if t != -1]

                if probs.shape[1] != len(filtered_topics):
                    # Column count no longer aligns with topic ids (e.g. topics
                    # were reduced after probabilities were computed) -> fall
                    # back to hard assignments rather than mislabel documents.
                    for t in topics:
                        doc_topics.append({t: 1.0})
                else:
                    for doc_prob in probs:
                        # Map prob index to actual topic_id
                        doc_map = {filtered_topics[i]: float(prob) for i, prob in enumerate(doc_prob)}
                        doc_topics.append(doc_map)
            else:
                # Fallback to hard assignment
                for t in topics:
                    doc_topics.append({t: 1.0})

            # 3. Metadata & Model Info
            metadata = {
                'model': model,
                'texts': texts,
                'num_topics': len(topic_ids)  # excludes the -1 outliers topic
            }

            model_info = {
                'algorithm': self.algorithm_name,
                'version': bertopic.__version__,
                'params': str(params),
                'num_documents': str(len(texts)),
                'num_topics': str(len(topic_ids))
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
