import threading
from dataclasses import replace
from typing import Any, Dict, List, Optional
from app.models.app_state import AppState
from app.models.services.data_loader import DataLoader
from app.models.services.exporter import Exporter
from app.models.services.visualizer import TopicVisualizer
from app.models.services.project_service import ProjectService
from app.models.services.topic_quality import compute_topic_quality
from app.models.services.static_viz import save_static_charts
from app.models.algorithms import get_algorithm


class AppController:
    """Handle user interactions for project setup, file selection, and project management."""

    def __init__(self, state: AppState):
        self.appState: AppState = state
        self.loader = DataLoader()
        self.exporter = Exporter()
        self.visualizer = TopicVisualizer()
        self.project_service = ProjectService()
        # Ensure the current algorithm's defaults are present from startup so
        # the main-window retrain path trains with the same parameters as the
        # wizard's "Default Settings" (audit H2/H6).
        if not state.algorithm_params:
            try:
                state.algorithm_params = get_algorithm(state.selected_algorithm).get_default_params()
            except Exception:
                pass  # leave empty; train() falls back to its own defaults

    def on_file_selected(self, file_path: str) -> None:
        """Handle file selection and update state with preview and guidance."""
        validation = self.loader.validate_file(file_path)

        if not validation.is_valid:
            self.appState.analysis_error = validation.error
            self.appState.notify()
            return

        # Update state
        self.appState.selected_file_path = file_path
        self.appState.file_preview = self.loader.load_preview(file_path)
        self.appState.analysis_error = None

        # Note: we could store validation.warnings in state if we have a UI for them
        self.appState.notify()

    def on_algorithm_changed(self, algorithm_name: str) -> None:
        """Handle algorithm switch and reset parameters."""
        try:
            algo = get_algorithm(algorithm_name)
            self.appState.selected_algorithm = algorithm_name
            self.appState.algorithm_params = algo.get_default_params()
            self.appState.notify()
        except ValueError as e:
            self.appState.analysis_error = str(e)
            self.appState.notify()

    def on_param_changed(self, param_name: str, value: Any) -> None:
        """Handle parameter adjustment."""
        self.appState.algorithm_params[param_name] = value
        self.appState.notify()

    def set_params(self, params: Dict[str, Any]) -> None:
        """Apply a batch of parameter values to state (wizard Train, custom mode)."""
        self.appState.algorithm_params.update(params)
        self.appState.notify()

    def get_param_schema(self, algorithm_name: str) -> Dict[str, Any]:
        """Return an algorithm's parameter schema. Views must not call the model directly."""
        return get_algorithm(algorithm_name).get_param_schema()

    def get_static_chart_path(self, viz_name: str) -> Optional[str]:
        """Return the pre-generated static chart PNG path for a visualization,
        or None if no result/chart exists (v0.3.0, WP1)."""
        result = self.appState.current_result
        if result is None:
            return None
        return result.metadata.get("static_chart_paths", {}).get(viz_name)

    def open_interactive_viz(self, viz_name: str) -> None:
        """Open the pre-generated offline HTML for a visualization in the
        default browser (v0.3.0, WP1)."""
        result = self.appState.current_result
        if result is None:
            return
        path = result.metadata.get("viz_files", {}).get(viz_name)
        if path:
            self.visualizer.open_visualization(path)

    # Topic refinement (v0.4.0, WP1)
    def merge_topics(self, topic_ids: List[int]) -> None:
        """Merge the selected topics into one; re-derives metrics + viz."""
        result = self.appState.current_result
        if result is None:
            return
        self._start_refinement(
            lambda: get_algorithm(self.appState.selected_algorithm).merge_topics(result, topic_ids)
        )

    def delete_topics(self, topic_ids: List[int]) -> None:
        """Delete the selected topics (documents → outlier -1); re-derives metrics + viz."""
        result = self.appState.current_result
        if result is None:
            return
        self._start_refinement(
            lambda: get_algorithm(self.appState.selected_algorithm).delete_topics(result, topic_ids)
        )

    def label_topic(self, topic_id: int, label: str) -> None:
        """Store a user interpretation for a topic (no model mutation)."""
        result = self.appState.current_result
        if result is None:
            return
        labels = dict(result.topic_labels or {})
        labels[topic_id] = label
        self.appState.current_result = replace(result, topic_labels=labels)
        self.appState.notify()

    def _start_refinement(self, mutate) -> None:
        """Run a refinement (mutate model → re-derive metrics + viz) in a background thread."""
        self.appState.analysis_in_progress = True
        self.appState.analysis_status = "Refining topics..."
        self.appState.notify()
        threading.Thread(target=self._refine_worker, args=(mutate,), daemon=True).start()

    def _refine_worker(self, mutate) -> None:
        """Background: mutate the model, rebuild the result, re-derive metrics + viz."""
        try:
            new_result = mutate()
            try:
                top_n = int(self.appState.algorithm_params.get('bertopic_top_n_words', 10))
                new_result.quality_metrics = compute_topic_quality(
                    new_result.topics, new_result.metadata.get('texts', []), top_n=top_n)
            except Exception:
                new_result.quality_metrics = None
            try:
                new_result.metadata['static_chart_paths'] = save_static_charts(
                    new_result.metadata.get('model'), self.visualizer.output_dir)
                new_result.metadata['viz_files'] = self.visualizer.visualize(
                    new_result, self.appState.selected_algorithm)
            except Exception:
                new_result.metadata['static_chart_paths'] = {}
                new_result.metadata['viz_files'] = {}
            self.appState.current_result = new_result
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.appState.analysis_error = f"Refinement failed: {str(e)}"
        finally:
            self.appState.analysis_in_progress = False
            self.appState.analysis_status = ""
            self.appState.notify()

    def export_csv(self, output_path: str) -> None:
        """Export the current TopicResult to CSV."""
        if self.appState.current_result:
            self.exporter.to_csv(self.appState.current_result, output_path)

    def export_json(self, output_path: str) -> None:
        """Export the current TopicResult to JSON (audit M4)."""
        if self.appState.current_result:
            self.exporter.to_json(self.appState.current_result, output_path)

    def export_methodology_report(self, output_path: str) -> None:
        """Export the methodology report for the current TopicResult."""
        if self.appState.current_result:
            self.exporter.generate_methodology_report(self.appState.current_result, output_path)

    def export_visualizations(self) -> Optional[str]:
        """Generate offline HTML visualizations and open them in the browser.

        Returns an error message if nothing was exported, else None.
        Safe to call from a background thread; only touches the model and
        file system, never Tkinter (audit M1/M4).
        """
        if not self.appState.current_result:
            return "No analysis results to visualize."
        viz_files = self.visualizer.visualize(
            self.appState.current_result, self.appState.selected_algorithm
        )
        if not viz_files:
            return "No visualizations could be generated for this result."
        for path in viz_files.values():
            self.visualizer.open_visualization(path)
        return None

    def save_project(self, output_path: str) -> None:
        """Save current session to file."""
        try:
            self.project_service.save_project(self.appState, output_path)
        except Exception as e:
            self.appState.analysis_error = f"Save failed: {str(e)}"
            self.appState.notify()

    def load_project(self, input_path: str) -> None:
        """Load session from file."""
        try:
            self.project_service.load_project(input_path, self.appState)
            self.appState.notify()
        except Exception as e:
            self.appState.analysis_error = f"Load failed: {str(e)}"
            self.appState.notify()
