import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from typing import Dict, Any
from app.models.app_state import AppState
from app.controllers.app_controller import AppController
from app.controllers.analysis_controller import AnalysisController
from app.models.algorithms import get_algorithm
from app.views.panels.hyperparams.bertopic_section import BERTopicSection
from app.views.panels.hyperparams.umap_section import UMAPSection
from app.views.panels.hyperparams.hdbscan_section import HDBSCANSection

class AlgorithmSettingsPanel(ttk.Frame):
    """Panel for configuring algorithm parameters."""

    def __init__(self, parent, state: AppState, controller: AppController, analysis_controller: AnalysisController):
        super().__init__(parent, padding=10)
        self.appState: AppState = state
        self.controller = controller
        self.analysis_controller = analysis_controller

        self.appState.subscribe(self._on_state_changed)
        self._build_ui()
        self._render()

    def _build_ui(self):
        self.lbl_title = ttk.Label(self, text="Algorithm Parameters", font=("Helvetica", 12, "bold"))
        self.lbl_title.pack(pady=10)

        # Retrain Button
        self.btn_retrain = ttk.Button(
            self,
            text="Retrain Model with Current Params",
            bootstyle="success",
            command=self._on_retrain
        )
        self.btn_retrain.pack(pady=(0, 20))

        # --- Scrollable Area Implementation ---
        self.container = ttk.Frame(self)
        self.container.pack(fill=BOTH, expand=YES, pady=10)

        self.canvas = ttk.Canvas(self.container, highlightthickness=0)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=YES)

        self.scrollbar = ttk.Scrollbar(self.container, orient=VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollable_frame = ttk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def _on_retrain(self):
        """Trigger a new analysis run using the current hyperparameters."""
        if not self.appState.selected_file_path:
            from tkinter import messagebox
            messagebox.showwarning("No File Selected", "Please select a data file before retraining.")
            return

        # 1. Show loading panel via MainWindow
        root = self.winfo_toplevel()
        if hasattr(root, 'show_loading_panel'):
            root.show_loading_panel()

        # 2. Trigger the analysis pipeline
        self.analysis_controller.run_analysis()

    def _on_state_changed(self, state: AppState):
        self._render()

    def _render(self):
        # Update retrain button state
        can_retrain = (
            self.appState.selected_file_path is not None and
            not self.appState.analysis_in_progress
        )
        self.btn_retrain.config(state="normal" if can_retrain else "disabled")

        # Clear existing parameters in the scrollable frame
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        if self.appState.selected_algorithm == "BERTopic":
            # Use modular sections for BERTopic
            # display only if we have the result from training
            if self.appState.current_result:
                BERTopicSection(self.scrollable_frame, self.appState, self.controller).pack(fill=X, pady=10)
                UMAPSection(self.scrollable_frame, self.appState, self.controller).pack(fill=X, pady=10)
                HDBSCANSection(self.scrollable_frame, self.appState, self.controller).pack(fill=X, pady=10)
        else:
            # Generic fallback for other algorithms
            try:
                algo = get_algorithm(self.appState.selected_algorithm)
                schema = algo.get_param_schema()
                self._build_param_form(schema)
            except Exception:
                # Fallback mock content if algorithm not ready
                ttk.Label(
                    self.scrollable_frame,
                    text="[Mock-up Content]\nParameter forms and\nconfiguration will\nbe here.",
                    justify=LEFT
                ).pack(pady=5)

    def _build_param_form(self, schema: Dict[str, Any]):
        for param_name, config in schema.items():
            row = ttk.Frame(self.scrollable_frame)
            row.pack(fill=X, pady=2)

            lbl = ttk.Label(row, text=f"{param_name}:", width=12)
            lbl.pack(side=LEFT, padx=2)

            p_type = config.get('type')
            current_val = self.appState.algorithm_params.get(param_name, config.get('default'))

            if p_type == 'int' or p_type == 'float':
                var = ttk.IntVar(value=current_val) if p_type == 'int' else ttk.DoubleVar(value=current_val)
                entry = ttk.Entry(row, textvariable=var, width=5)
                entry.pack(side=RIGHT, padx=0)
                var.trace_add("write", lambda *args, p=param_name, v=var: self.controller.on_param_changed(p, v.get()))

            elif p_type == 'choice':
                var = ttk.StringVar(value=current_val)
                combo = ttk.Combobox(row, textvariable=var, values=config.get('options', []), state="readonly", width=15)
                combo.pack(side=RIGHT, padx=0)
                combo.bind("<<ComboboxSelected>>", lambda e, p=param_name, v=var: self.controller.on_param_changed(p, v.get()))
