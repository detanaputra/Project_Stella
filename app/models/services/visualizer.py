import os
import webbrowser
from typing import Dict, Optional
from app.models.topic_result import TopicResult

class TopicVisualizer:
    """Generate interactive visualizations for export to browser (offline HTML)."""

    # BERTopic model methods that take no extra arguments and produce a
    # standalone Plotly figure. Real plots, not placeholders (audit M4).
    _VIZ_METHODS = [
        ("topics", "visualize_topics"),
        ("heatmap", "visualize_heatmap"),
        ("barchart", "visualize_barchart"),
        ("hierarchy", "visualize_hierarchy"),
    ]

    def __init__(self, output_dir: Optional[str] = None):
        # Matches the documented default (~/.bertopic-gui/viz) so exports land
        # in a stable, user-level location rather than a cwd-relative path.
        self.output_dir = output_dir or os.path.join(os.path.expanduser("~"), ".bertopic-gui", "viz")
        os.makedirs(self.output_dir, exist_ok=True)

    def visualize(self, result: TopicResult, algorithm_name: str) -> Dict[str, str]:
        """
        Generate real Plotly visualizations as standalone, offline HTML files.

        Args:
            result: TopicResult
            algorithm_name: "BERTopic", "LDA", etc.

        Returns:
            Dict mapping viz_type -> file_path. Empty if the algorithm or
            model metadata does not support visualization. Visualizations that
            fail individually are skipped.
        """
        if algorithm_name != "BERTopic" or 'model' not in result.metadata:
            return {}

        model = result.metadata['model']
        os.makedirs(self.output_dir, exist_ok=True)

        viz_files = {}
        for name, method in self._VIZ_METHODS:
            viz_func = getattr(model, method, None)
            if viz_func is None:
                continue
            try:
                fig = viz_func()
                path = os.path.join(self.output_dir, f"{name}.html")
                # Embed plotly.js so the file works fully offline (audit M5).
                fig.write_html(path, include_plotlyjs=True, full_html=True)
                viz_files[name] = path
            except Exception:
                # Skip a single failing visualization rather than failing all.
                continue

        return viz_files

    def visualize_one(self, result: TopicResult, viz_name: str) -> Optional[str]:
        """Generate one visualization's offline HTML; return the file path or None.

        Used by the "Open interactive" button on the static viz tabs (v0.3.0,
        WP1). Individual failures return None rather than raising.
        """
        if 'model' not in result.metadata:
            return None
        model = result.metadata['model']
        method = getattr(model, f"visualize_{viz_name}", None)
        if method is None:
            return None
        try:
            fig = method()
            path = os.path.join(self.output_dir, f"{viz_name}.html")
            fig.write_html(path, include_plotlyjs=True, full_html=True)
            return path
        except Exception:
            return None

    def open_visualization(self, file_path: str) -> None:
        """Open a visualization file in the default browser."""
        webbrowser.open(f"file://{os.path.abspath(file_path)}")
