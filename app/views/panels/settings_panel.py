import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from typing import Dict, Any
from app.models.app_state import AppState
from app.controllers.app_controller import AppController
from app.models.algorithms import get_algorithm
from app.views.panels.hyperparams.bertopic_section import BERTopicSection
from app.views.panels.hyperparams.umap_section import UMAPSection
from app.views.panels.hyperparams.hdbscan_section import HDBSCANSection

class SettingsPanel(ttk.Frame):
    """Panel for algorithm selection and parameter configuration."""

    def __init__(self, parent, state: AppState, controller: AppController):
        super().__init__(parent)
        self.appState: AppState = state
        self.controller = controller

        self.appState.subscribe(self._on_state_changed)
        self._build_ui()
        self._render()

    def _build_ui(self):
        self.frame = ttk.Frame(self)
        self.frame.pack(fill=X, pady=5)

        self.lbl_title = ttk.Label(self.frame, text="2. Configure Algorithm", font=("Helvetica", 12, "bold"))
        self.lbl_title.pack(side=LEFT, padx=5)

        # Algorithm dropdown
        self.algo_var = ttk.StringVar()
        self.combo_algo = ttk.Combobox(
            self.frame,
            textvariable=self.algo_var,
            values=["BERTopic"], # Updated dynamically in _render
            state="readonly",
            width=20
        )
        self.combo_algo.pack(side=LEFT, padx=10)
        self.combo_algo.bind("<<ComboboxSelected>>", self._on_algo_selected)

        # Container for dynamic params
        self.params_container = ttk.Frame(self)
        self.params_container.pack(fill=X, pady=10)

    def _on_algo_selected(self, event):
        algo_name = self.combo_algo.get()
        self.controller.on_algorithm_changed(algo_name)

    def _on_state_changed(self, state: AppState):
        self._render()

    def _render(self):
        # Update dropdown
        self.algo_var.set(self.appState.selected_algorithm)
        # In a real app, we'd get this list from AVAILABLE_ALGORITHMS
        self.combo_algo['values'] = ("BERTopic",)

        # Clear and rebuild param form
        for widget in self.params_container.winfo_children():
            widget.destroy()

        if self.appState.selected_algorithm == "BERTopic":
            # Use modular sections for BERTopic
            BERTopicSection(self.params_container, self.appState, self.controller).pack(fill=X, pady=10)
            UMAPSection(self.params_container, self.appState, self.controller).pack(fill=X, pady=10)
            HDBSCANSection(self.params_container, self.appState, self.controller).pack(fill=X, pady=10)
        else:
            # Generic fallback for other algorithms
            try:
                algo = get_algorithm(self.appState.selected_algorithm)
                schema = algo.get_param_schema()
                self._build_param_form(schema)
            except Exception:
                ttk.Label(self.params_container, text="Error loading parameters").pack()

    def _build_param_form(self, schema: Dict[str, Any]):
        for param_name, config in schema.items():
            row = ttk.Frame(self.params_container)
            row.pack(fill=X, pady=2)

            lbl = ttk.Label(row, text=f"{param_name} ({config.get('tooltip', '')}):", width=40)
            lbl.pack(side=LEFT, padx=5)

            p_type = config.get('type')
            current_val = self.appState.algorithm_params.get(param_name, config.get('default'))

            if p_type == 'int' or p_type == 'float':
                var = ttk.IntVar(value=current_val) if p_type == 'int' else ttk.DoubleVar(value=current_val)
                entry = ttk.Entry(row, textvariable=var, width=10)
                entry.pack(side=LEFT, padx=5)
                # Trigger update on change
                var.trace_add("write", lambda *args, p=param_name, v=var: self.controller.on_param_changed(p, v.get()))

            elif p_type == 'choice':
                var = ttk.StringVar(value=current_val)
                combo = ttk.Combobox(row, textvariable=var, values=config.get('options', []), state="readonly", width=15)
                combo.pack(side=LEFT, padx=5)
                combo.bind("<<ComboboxSelected>>", lambda e, p=param_name, v=var: self.controller.on_param_changed(p, v.get()))
