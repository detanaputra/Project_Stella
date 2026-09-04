import multiprocessing
import os
import tempfile
import threading
from tkinter import messagebox
from typing import Any, Dict, Optional
from app.models.app_state import AppState
from app.models.services.data_loader import DataLoader
from app.models.services.exporter import Exporter
from app.models.services.visualizer import TopicVisualizer
from app.models.services.static_viz import static_chart
from app.models.services.project_service import ProjectService
from app.models.algorithms import get_algorithm


def _launch_bertopic_webview(html_path: str, title: str) -> None:
    """
    Top-level function to launch the pywebview window.

    Must be global (module-level) so multiprocessing can pickle it. Owned by
    the controller so views contain no process-launch logic.
    """
    import webview

    # OS-level DPI awareness for Windows to prevent overall window blur
    if os.name == 'nt':
        import ctypes
        try:
            # Per-Monitor V2 DPI Awareness (Windows 10 1703+)
            ctypes.windll.user32.SetProcessDpiAwarenessContext(-4)
        except Exception:
            try:
                # Per-Monitor DPI Awareness
                ctypes.windll.shcore.SetProcessDpiAwareness(2)
            except Exception:
                try:
                    # System DPI Awareness
                    ctypes.windll.user32.SetProcessDPIAware()
                except Exception:
                    pass

    try:
        window = webview.create_window(
            title,
            url=f'file://{html_path}',
            width=1000,
            height=800
        )
        webview.start()
    finally:
        # Clean up the temporary file after the window is closed
        if os.path.exists(html_path):
            try:
                os.remove(html_path)
            except Exception:
                pass


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

    def request_visualization(self, method_name: str, title: str) -> None:
        """Generate and launch a BERTopic visualization in a separate process.

        Owns the loading state (analysis_in_progress) and all model/file/process
        logic — the panel only calls this. Safe from the UI thread; the heavy
        work runs in a background thread.
        """
        self.appState.analysis_in_progress = True
        self.appState.analysis_status = f"Generating {title}..."
        self.appState.notify()
        threading.Thread(
            target=self._generate_visualization,
            args=(method_name, title),
            daemon=True
        ).start()

    def _generate_visualization(self, method_name: str, title: str) -> None:
        """Background task: build the Plotly HTML and launch the webview process."""
        try:
            # Retrieve BERTopic model from metadata
            model = self.appState.current_result.metadata.get('model')
            if model is None:
                self.appState.call_on_main(
                    lambda: messagebox.showerror("Error", "BERTopic model not found in current results.")
                )
                return

            # Dynamically call the requested BERTopic visualization method
            viz_func = getattr(model, method_name, None)
            if viz_func is None:
                self.appState.call_on_main(
                    lambda: messagebox.showerror("Error", f"Method {method_name} not available in this model.")
                )
                return

            # Generate the Plotly figure
            fig = viz_func()

            # plotly.js is embedded (not CDN) so the visualization works offline
            # (audit M5). High-DPI + responsive config avoids blurry output.
            html_content = fig.to_html(
                include_plotlyjs=True,
                full_html=True,
                config={
                    'plotGlPixelRatio': 2,  # Forces higher resolution for WebGL (Retina fix)
                    'responsive': True      # Prevents CSS-based stretching blur
                },
                default_width='100%',
                default_height='100%'
            )

            # Create a temporary file
            with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html', encoding='utf-8') as f:
                f.write(html_content)
                temp_path = f.name

            # Launch the webview in a separate PROCESS
            p = multiprocessing.Process(
                target=_launch_bertopic_webview,
                args=(temp_path, title),
                daemon=True
            )
            p.start()

        except Exception as e:
            self.appState.call_on_main(
                lambda: messagebox.showerror("Visualization Error", f"An error occurred:\n{str(e)}")
            )

        finally:
            # Dismiss loading state
            self.appState.analysis_in_progress = False
            self.appState.analysis_status = ""
            self.appState.notify()

    def render_static_chart(self, viz_name: str, figure) -> bool:
        """Draw a static matplotlib chart for the current result onto ``figure``.

        Returns True on success, False if there is no result/model or rendering
        failed. The view owns the canvas; this only touches the model (v0.3.0,
        WP1).
        """
        result = self.appState.current_result
        if result is None:
            return False
        model = result.metadata.get("model")
        if model is None:
            return False
        try:
            static_chart(model, viz_name, figure=figure)
            return True
        except Exception:
            return False

    def open_interactive_viz(self, viz_name: str) -> None:
        """Generate one visualization's offline HTML and open it in the default
        browser (the "Open interactive" button on the static viz tabs, v0.3.0,
        WP1)."""
        if not self.appState.current_result:
            return
        path = self.visualizer.visualize_one(self.appState.current_result, viz_name)
        if path:
            self.visualizer.open_visualization(path)

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
