import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from app.models.app_state import AppState
from app.controllers.app_controller import AppController

class SummaryPanel(ttk.Frame):
    """Step 4: Final summary of configuration before training."""

    def __init__(self, parent, state: AppState, controller: AppController):
        super().__init__(parent, padding=20)
        self.appState: AppState = state
        self.controller = controller

        self._build_ui()

    def _build_ui(self):
        ttk.Label(self, text="Ready to Train", font=("Helvetica", 14, "bold")).pack(pady=(0, 20))

        # Summary Container
        self.summary_container = ttk.Frame(self)
        self.summary_container.pack(fill=BOTH, expand=YES, pady=10)

        # Placeholder for dynamic summary
        self.summary_text = ttk.Label(
            self.summary_container,
            text="Please complete previous steps...",
            font=("Helvetica", 11),
            justify=LEFT
        )
        self.summary_text.pack(anchor=W)

    def update_summary(self, config: dict):
        """
        Updates the display with the final selections.

        Args:
            config: Dictionary containing 'algorithm', 'file_path',
                    'settings_mode', and 'params'.
        """
        summary = (
            f"Algorithm: {config.get('algorithm')}\n\n"
            f"Data File: {config.get('file_path')}\n\n"
            f"Settings: {config.get('settings_mode').capitalize()}\n\n"
            f"Model: {config.get('params', {}).get('bertopic_embedding_model', 'Default')}"
        )
        self.summary_text.config(text=summary)
