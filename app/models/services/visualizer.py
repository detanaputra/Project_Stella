import functools
import http.server
import os
import threading
import webbrowser
from typing import Dict, Optional
from app.models.topic_result import TopicResult


class _QuietHandler(http.server.SimpleHTTPRequestHandler):
    """Serves files without logging each request to stderr."""

    def log_message(self, format, *args):
        pass


class _VizServer:
    """A tiny local HTTP server serving the visualisation output directory.

    Browsers handle http://localhost URLs far more reliably than file:// URLs
    (which intermittently open a blank tab), so interactive visualisations are
    served over localhost instead of opened as local files (v0.3.0, WP1).
    """

    def __init__(self, directory: str):
        handler = functools.partial(_QuietHandler, directory=directory)
        self._httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
        self.port = self._httpd.server_address[1]
        self._thread = threading.Thread(target=self._httpd.serve_forever, daemon=True)
        self._thread.start()

    def url_for(self, filename: str) -> str:
        return f"http://localhost:{self.port}/{filename}"

class TopicVisualizer:
    """Generate interactive visualizations for export to browser (offline HTML)."""

    # BERTopic model methods that take no extra arguments and produce a
    # standalone Plotly figure. Real plots, not placeholders (audit M4).
    _VIZ_METHODS = [
        ("topics", "visualize_topics"),
        ("heatmap", "visualize_heatmap"),
        ("barchart", "visualize_barchart"),
        ("hierarchy", "visualize_hierarchy"),
        ("term_rank", "visualize_term_rank"),
    ]

    def __init__(self, output_dir: Optional[str] = None):
        # Matches the documented default (~/.bertopic-gui/viz) so exports land
        # in a stable, user-level location rather than a cwd-relative path.
        self.output_dir = output_dir or os.path.join(os.path.expanduser("~"), ".bertopic-gui", "viz")
        os.makedirs(self.output_dir, exist_ok=True)
        self._server = None  # local HTTP server, started lazily on first open

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

    def _ensure_server(self) -> _VizServer:
        """Start the local HTTP server once, on first use."""
        if self._server is None:
            self._server = _VizServer(self.output_dir)
        return self._server

    def open_visualization(self, file_path: str) -> None:
        """Open a visualization in the default browser, served over localhost.

        Served over http://localhost rather than file:// because browsers handle
        http URLs reliably (file:// intermittently opens a blank tab).
        """
        server = self._ensure_server()
        webbrowser.open(server.url_for(os.path.basename(file_path)))
