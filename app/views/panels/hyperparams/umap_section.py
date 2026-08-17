import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from app.views.panels.hyperparams.base_section import BaseHyperparamSection

class UMAPSection(BaseHyperparamSection):
    """UI section for UMAP-specific hyperparameters."""

    def __init__(self, parent, state, controller):
        super().__init__(parent, state, controller)

        self.container = ttk.LabelFrame(self, text="UMAP", padding=10)
        self.container.pack(fill=X, expand=YES)

        # --- N Neighbors ---
        n_neigh_frame = ttk.Frame(self.container)
        n_neigh_frame.pack(fill=X, pady=5)
        ttk.Label(n_neigh_frame, text="N Neighbors:", width=20).pack(side=LEFT)
        self.n_neigh_var = ttk.IntVar(value=state.algorithm_params.get('umap_n_neighbors', 15))
        self._bind_param(self.n_neigh_var, 'umap_n_neighbors')
        self.n_neigh_spin = ttk.Spinbox(n_neigh_frame, from_=2, to=100, textvariable=self.n_neigh_var, width=10)
        self.n_neigh_spin.pack(side=LEFT)

        # --- N Components ---
        n_comp_frame = ttk.Frame(self.container)
        n_comp_frame.pack(fill=X, pady=5)
        ttk.Label(n_comp_frame, text="N Components:", width=20).pack(side=LEFT)
        self.n_comp_var = ttk.IntVar(value=state.algorithm_params.get('umap_n_components', 5))
        self._bind_param(self.n_comp_var, 'umap_n_components')
        self.n_comp_spin = ttk.Spinbox(n_comp_frame, from_=2, to=50, textvariable=self.n_comp_var, width=10)
        self.n_comp_spin.pack(side=LEFT)

        # --- Metric ---
        metric_frame = ttk.Frame(self.container)
        metric_frame.pack(fill=X, pady=5)
        ttk.Label(metric_frame, text="Metric:", width=20).pack(side=LEFT)
        self.metric_var = ttk.StringVar(value=state.algorithm_params.get('umap_metric', 'cosine'))
        self._bind_param(self.metric_var, 'umap_metric')
        self.metric_combo = ttk.Combobox(
            metric_frame,
            textvariable=self.metric_var,
            values=["cosine", "euclidean", "manhattan", "chebyshev", "minkowski"],
            state="readonly"
        )
        self.metric_combo.pack(side=LEFT, fill=X, expand=YES)

        # --- Low Memory ---
        low_mem_frame = ttk.Frame(self.container)
        low_mem_frame.pack(fill=X, pady=5)
        self.low_mem_var = ttk.BooleanVar(value=state.algorithm_params.get('umap_low_memory', False))
        self._bind_param(self.low_mem_var, 'umap_low_memory')
        self.low_mem_check = ttk.Checkbutton(low_mem_frame, text="Low Memory Mode", variable=self.low_mem_var)
        self.low_mem_check.pack(side=LEFT)

    def get_params(self) -> dict:
        return {
            "umap_n_neighbors": self.n_neigh_var.get(),
            "umap_n_components": self.n_comp_var.get(),
            "umap_metric": self.metric_var.get(),
            "umap_low_memory": self.low_mem_var.get()
        }
