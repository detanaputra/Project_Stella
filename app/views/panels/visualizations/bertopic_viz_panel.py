import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import webview
import multiprocessing
import threading
import tempfile
import os
from tkinter import messagebox
from app.models.app_state import AppState
from app.controllers.app_controller import AppController

def _launch_bertopic_webview(html_path, title):
    """
    Top-level function to launch the pywebview window.
    Must be global for multiprocessing to pickle it.
    """
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
        # Create the window
        window = webview.create_window(
            title,
            url=f'file://{html_path}',
            width=1000,
            height=800
        )
        # Start the webview loop
        webview.start()
    finally:
        # Clean up the temporary file after the window is closed
        if os.path.exists(html_path):
            try:
                os.remove(html_path)
            except Exception:
                pass

class BERTopicVisualisation(ttk.Frame):
    """Panel for launching BERTopic interactive visualizations."""

    def __init__(self, parent, state: AppState, controller: AppController):
        super().__init__(parent, padding=10)
        self.appState: AppState = state
        self.controller = controller

        self._build_ui()

    def _build_ui(self):
        # Section Title
        ttk.Label(
            self,
            text="BERTopic Visualizations",
            font=("Helvetica", 11, "bold")
        ).pack(anchor=W, pady=(0, 10))

        # Visualization Buttons Frame
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill=X)

        # Define the visualizations to implement
        # (Button Text, Model Method, Window Title)
        viz_configs = [
            ("Visualize Topics", "visualize_topics", "Intertopic Distance Map"),
            ("Visualize Heatmap", "visualize_heatmap", "Topic Heatmap"),
            ("Visualize Bar Chart", "visualize_barchart", "Topic Bar Chart"),
            ("Visualize Term Rank", "visualize_term_rank", "Term Ranking"),
            ("Visualize Hierarchy", "visualize_hierarchy", "Topic Hierarchy"),
        ]

        for text, method, title in viz_configs:
            btn = ttk.Button(
                btn_frame,
                text=text,
                bootstyle="info-outline",
                command=lambda t=text, m=method, tl=title: self._on_request_visualization(m, tl)
            )
            btn.pack(fill=X, pady=5)

    def _on_request_visualization(self, method_name, title):
        """Initiate the visualization process with a loading indicator."""
        if not self.appState.current_result:
            messagebox.showwarning("No Analysis", "Please run an analysis first before visualizing.")
            return

        # 1. Trigger loading state
        self.appState.analysis_in_progress = True
        self.appState.analysis_status = f"Generating {title}..."
        self.appState.notify()

        # 2. Display the loading panel
        root = self.winfo_toplevel()
        if hasattr(root, 'show_loading_panel'):
            root.show_loading_panel()

        # 3. Run the heavy lifting in a background thread
        threading.Thread(
            target=self._process_visualization,
            args=(method_name, title),
            daemon=True
        ).start()

    def _process_visualization(self, method_name, title):
        """Background task to generate HTML and launch the webview process."""
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

            # Convert Plotly figure to HTML with High DPI and responsiveness
            # configurations. plotly.js is embedded (not CDN) so the
            # visualization works offline (audit M5).
            html_content = fig.to_html(
                include_plotlyjs=True,
                full_html=True,
                config={
                    'plotGlPixelRatio': 2, # Forces higher resolution for WebGL (Retina fix)
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
            # 4. Dismiss loading state
            self.appState.analysis_in_progress = False
            self.appState.analysis_status = ""
            self.appState.notify()
