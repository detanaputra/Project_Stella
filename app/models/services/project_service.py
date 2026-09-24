import json
import os
import shutil
import tempfile
import zipfile
from typing import Any, Dict, Optional

from app.models.app_state import AppState
from app.models.topic_result import TopicResult
from app.models.algorithms import AVAILABLE_ALGORITHMS, get_algorithm


class ProjectService:
    """Save/load projects as a single-file zip bundle (v0.5.0, WP3).

    A ``.stella`` file is a zip archive containing:
      project.json          — state + a ``models`` dict keyed by model_id, each
                              with its selected_algorithm, algorithm_params, and
                              full result data (topics, doc_topics, quality_metrics,
                              model_info, topic_labels, texts, original_texts)
      model/{model_id}/     — the trained model (per-algorithm native save)
      viz/{model_id}/       — the 5 PNGs + 5 HTMLs

    The ``models`` dict is multi-model-ready: adding a model is another key.
    On load, the bundle is extracted to ``~/.stella/{model_id}/`` (a persistent
    location the viz tabs and refinement can read), and the result is rebuilt
    with the model loaded.
    """

    #: Where loaded projects' model + viz files are extracted (per model id).
    STELLA_DIR = os.path.join(os.path.expanduser("~"), ".stella")

    def save_project(self, state: AppState, output_path: str) -> str:
        """Serialize state + result into a zip bundle at output_path."""
        result = state.current_result
        models = {}
        if result is not None:
            model_id = result.model_id or "model"
            models[model_id] = {
                "selected_algorithm": state.selected_algorithm,
                "algorithm_params": state.algorithm_params,
                "result": self._serialize_result(result),
            }
        project_data = {
            "selected_file_path": state.selected_file_path,
            "models": models,
        }
        with tempfile.TemporaryDirectory() as tmp:
            with open(os.path.join(tmp, "project.json"), "w", encoding="utf-8") as f:
                json.dump(project_data, f, indent=4)
            if result is not None and result.metadata.get("model") is not None:
                model_dir = os.path.join(tmp, "model", result.model_id or "model")
                os.makedirs(model_dir, exist_ok=True)
                get_algorithm(state.selected_algorithm).save_model(result.metadata["model"], model_dir)
            if result is not None:
                self._copy_viz(result, os.path.join(tmp, "viz", result.model_id or "model"))
            with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
                for root, _, files in os.walk(tmp):
                    for file in files:
                        full = os.path.join(root, file)
                        zf.write(full, os.path.relpath(full, tmp))
        return output_path

    def load_project(self, input_path: str, state: AppState) -> None:
        """Restore state + result from a zip bundle."""
        with zipfile.ZipFile(input_path, "r") as zf:
            data = json.loads(zf.read("project.json").decode("utf-8"))
            models = data.get("models") or {}
            # Single-model today: the one entry is the current model.
            model_id = next(iter(models)) if models else None
            dest = os.path.join(self.STELLA_DIR, model_id) if model_id else None
            if dest:
                os.makedirs(dest, exist_ok=True)
                zf.extractall(dest)

        # Restore the shared state
        file_path = data.get("selected_file_path")
        if file_path and not os.path.exists(file_path):
            file_path = None
        state.selected_file_path = file_path

        # Rebuild the current model (algorithm + params + result from its entry)
        if model_id and dest:
            model_data = models[model_id]
            algo = model_data.get("selected_algorithm", "BERTopic")
            if algo not in AVAILABLE_ALGORITHMS:
                algo = "BERTopic"
            state.selected_algorithm = algo
            loaded = model_data.get("algorithm_params")
            if not isinstance(loaded, dict):
                loaded = {}
            state.algorithm_params = {**get_algorithm(algo).get_default_params(), **loaded}
            result_data = model_data.get("result")
            if result_data:
                result = self._rebuild_result(result_data, algo, dest)
                result.metadata["params"] = state.algorithm_params
                state.current_result = result
            else:
                state.current_result = None
        else:
            state.current_result = None

    def _serialize_result(self, result: TopicResult) -> Dict[str, Any]:
        return {
            "topics": result.topics,
            "doc_topics": result.doc_topics,
            "model_info": result.model_info,
            "quality_metrics": result.quality_metrics,
            "topic_labels": result.topic_labels,
            "model_id": result.model_id,
            "texts": result.metadata.get("texts", []),
            "original_texts": result.metadata.get("original_texts", []),
        }

    def _copy_viz(self, result: TopicResult, viz_dir: str) -> None:
        os.makedirs(viz_dir, exist_ok=True)
        paths = list((result.metadata.get("viz_files") or {}).values()) + \
                list((result.metadata.get("static_chart_paths") or {}).values())
        for path in paths:
            if path and os.path.exists(path):
                shutil.copy(path, os.path.join(viz_dir, os.path.basename(path)))

    def _rebuild_result(self, data: Dict[str, Any], algo: str, dest: str) -> TopicResult:
        model_id = data.get("model_id")
        model = None
        if model_id:
            model_path = os.path.join(dest, "model", model_id)
            if os.path.exists(model_path):
                model = get_algorithm(algo).load_model(model_path)

        viz_files = {}
        static_chart_paths = {}
        viz_dir = os.path.join(dest, "viz", model_id) if model_id else None
        if viz_dir and os.path.isdir(viz_dir):
            for name in ("topics", "heatmap", "barchart", "hierarchy", "term_rank"):
                html = os.path.join(viz_dir, f"{name}.html")
                png = os.path.join(viz_dir, f"{name}.png")
                if os.path.exists(html):
                    viz_files[name] = html
                if os.path.exists(png):
                    static_chart_paths[name] = png

        # JSON object keys are strings; restore the int keys (topic ids).
        doc_topics = [
            {int(k): float(v) for k, v in doc.items()}
            for doc in data.get("doc_topics", [])
        ]
        topic_labels = {int(k): v for k, v in (data.get("topic_labels") or {}).items()}

        metadata = {
            "model": model,
            "texts": data.get("texts", []),
            "original_texts": data.get("original_texts", []),
            "num_topics": int((data.get("model_info") or {}).get("num_topics", 0)),
            "params": {},
            "static_chart_paths": static_chart_paths,
            "viz_files": viz_files,
        }
        return TopicResult(
            topics=data.get("topics", []),
            doc_topics=doc_topics,
            metadata=metadata,
            model_info=data.get("model_info", {}),
            quality_metrics=data.get("quality_metrics"),
            topic_labels=topic_labels,
            model_id=model_id,
        )
