import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from app.models.app_state import AppState
from app.controllers.app_controller import AppController

class BERTopicVisualisation(ttk.Frame):
    """Panel for launching BERTopic interactive visualizations.

    Thin view: it only checks state and asks the controller to run the
    visualization. All model calls, HTML generation, and process launching live
    in AppController.request_visualization (architecture: views call the
    controller; the controller runs the logic).
    """

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
        """Ask the controller to run the visualization with a loading indicator."""
        if not self.appState.current_result:
            messagebox.showwarning("No Analysis", "Please run an analysis first before visualizing.")
            return

        # Display the loading panel (UI concern; auto-closes when the
        # controller clears analysis_in_progress).
        root = self.winfo_toplevel()
        if hasattr(root, 'show_loading_panel'):
            root.show_loading_panel()

        # All generation logic lives in the controller (view stays thin).
        self.controller.request_visualization(method_name, title)
