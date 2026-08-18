import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from app.views.panels.hyperparams.base_section import BaseHyperparamSection

class HDBSCANSection(BaseHyperparamSection):
    """UI section for HDBSCAN-specific hyperparameters."""

    def __init__(self, parent, state, controller):
        super().__init__(parent, state, controller)

        self.container = ttk.LabelFrame(self, text="HDBSCAN", padding=10)
        self.container.pack(fill=X, expand=YES)

        # --- Min Samples ---
        min_samp_frame = ttk.Frame(self.container)
        min_samp_frame.pack(fill=X, pady=5)
        ttk.Label(min_samp_frame, text="Min Samples:", width=20).pack(side=LEFT)
        self.min_samp_var = ttk.IntVar(value=state.algorithm_params.get('hdbscan_min_samples', 10))
        self._bind_param(self.min_samp_var, 'hdbscan_min_samples')
        self.min_samp_spin = ttk.Spinbox(min_samp_frame, from_=1, to=100, textvariable=self.min_samp_var, width=10)
        self.min_samp_spin.pack(side=LEFT)

        # --- Min Cluster Size ---
        min_clust_frame = ttk.Frame(self.container)
        min_clust_frame.pack(fill=X, pady=5)
        ttk.Label(min_clust_frame, text="Min Cluster Size:", width=20).pack(side=LEFT)
        self.min_clust_var = ttk.IntVar(value=state.algorithm_params.get('hdbscan_min_cluster_size', 10))
        self._bind_param(self.min_clust_var, 'hdbscan_min_cluster_size')
        self.min_clust_spin = ttk.Spinbox(min_clust_frame, from_=1, to=100, textvariable=self.min_clust_var, width=10)
        self.min_clust_spin.pack(side=LEFT)

        # --- Metric ---
        metric_frame = ttk.Frame(self.container)
        metric_frame.pack(fill=X, pady=5)
        ttk.Label(metric_frame, text="Metric:", width=20).pack(side=LEFT)
        self.metric_var = ttk.StringVar(value=state.algorithm_params.get('hdbscan_metric', 'euclidean'))
        self._bind_param(self.metric_var, 'hdbscan_metric')
        self.metric_combo = ttk.Combobox(
            metric_frame,
            textvariable=self.metric_var,
            values=["euclidean", "manhattan", "chebyshev", "minkowski"],
            state="readonly"
        )
        self.metric_combo.pack(side=LEFT, fill=X, expand=YES)

    def get_params(self) -> dict:
        return {
            "hdbscan_min_samples": self.min_samp_var.get(),
            "hdbscan_min_cluster_size": self.min_clust_var.get(),
            "hdbscan_metric": self.metric_var.get()
        }
