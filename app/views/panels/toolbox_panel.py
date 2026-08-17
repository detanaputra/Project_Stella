import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from app.models.app_state import AppState
from app.controllers.app_controller import AppController
from app.views.panels.visualizations.bertopic_viz_panel import BERTopicVisualisation

class ToolboxPanel(ttk.Frame):
    """Panel providing quick access tools and options."""

    def __init__(self, parent, state: AppState, controller: AppController):
        super().__init__(parent, padding=10, bootstyle="secondary")
        self.appState: AppState = state
        self.controller = controller

        self._build_ui()

    def _build_ui(self):
        ttk.Label(self, text="Toolbox", font=("Helvetica", 12, "bold")).pack(pady=10)

        # BERTopic Visualizations Section
        self.viz_panel = BERTopicVisualisation(self, self.appState, self.controller)
        self.viz_panel.pack(fill=X, pady=10)
