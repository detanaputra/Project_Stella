import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from app.models.app_state import AppState
from app.controllers.app_controller import AppController
from app.views.panels.hyperparams.bertopic_section import BERTopicSection
from app.views.panels.hyperparams.umap_section import UMAPSection
from app.views.panels.hyperparams.hdbscan_section import HDBSCANSection

class HyperparamPanel(ttk.Frame):
    """Step 3: Hyperparameter configuration using modular sections."""

    def __init__(self, parent, state: AppState, controller: AppController):
        super().__init__(parent, padding=20)
        self.appState: AppState = state
        self.controller = controller

        self._build_ui()

    def _build_ui(self):
        ttk.Label(self, text="Hyperparameter Settings", font=("Helvetica", 14, "bold")).pack(pady=(0, 20))

        # --- Scrollable Area Implementation ---
        # 1. Create a container frame for canvas and scrollbar
        container = ttk.Frame(self)
        container.pack(fill=BOTH, expand=YES)

        # 2. Create Canvas
        self.canvas = ttk.Canvas(container, highlightthickness=8)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=YES)

        # 3. Create Scrollbar
        self.scrollbar = ttk.Scrollbar(container, orient=VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        # Configure canvas to use scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # 4. Create the internal frame that will actually hold the widgets
        self.scrollable_frame = ttk.Frame(self.canvas)

        # Add the frame to the canvas
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Ensure the interior frame expands to the canvas width
        self.canvas.bind("<Configure>", self._on_canvas_configure)

        # Update scrollregion when the frame size changes
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # --- Modular Sections ---
        self.sections = []

        # BERTopic General Settings
        self.bertopic_section = BERTopicSection(self.scrollable_frame, self.appState, self.controller)
        self.bertopic_section.pack(fill=X, pady=10)
        self.sections.append(self.bertopic_section)

        # UMAP Settings
        self.umap_section = UMAPSection(self.scrollable_frame, self.appState, self.controller)
        self.umap_section.pack(fill=X, pady=10)
        self.sections.append(self.umap_section)

        # HDBSCAN Settings
        self.hdbscan_section = HDBSCANSection(self.scrollable_frame, self.appState, self.controller)
        self.hdbscan_section.pack(fill=X, pady=10)
        self.sections.append(self.hdbscan_section)

        # Note about custom settings
        self.hint_label = ttk.Label(
            self,
            text="Note: These settings are applied if 'Custom Settings' was selected.",
            font=("Helvetica", 9, "italic"),
            bootstyle="secondary"
        )
        self.hint_label.pack(pady=20)

    def _on_canvas_configure(self, event):
        # Resize the interior frame to match the canvas width
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def get_current_params(self):
        """Aggregate parameters from all modular sections."""
        all_params = {}
        for section in self.sections:
            all_params.update(section.get_params())
        return all_params
