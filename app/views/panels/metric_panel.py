"""Metrics tab: topic quality gauges rendered with matplotlib.

Reads ``state.current_result.quality_metrics`` (computed by the pipeline in
the background, D-021) and draws one gauge/donut chart per metric. Follows the
cheap-subscriber discipline (D-022): it only re-renders when the result object
changes, never on every state change.
"""

from typing import Dict, Optional

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.patches import Wedge

from app.models.app_state import AppState
from app.controllers.app_controller import AppController


# Sentinel distinct from None: a guard keyed on None collides with the
# legitimate "no result yet" state (D-014).
_UNSET = object()

# Per-metric display config: label, (vmin, vmax) scale, gauge color.
_METRIC_CONFIG = {
    "npmi": ("NPMI Coherence", (-1.0, 1.0), "#2e86de"),
    "c_v": ("C_V Coherence", (0.0, 1.0), "#10ac84"),
    "u_mass": ("UMass Coherence", (-10.0, 0.0), "#ee5253"),
    "topic_diversity": ("Topic Diversity", (0.0, 1.0), "#feca57"),
}


class MetricPanel(ttk.Frame):
    """Display topic quality metrics as gauge/donut charts (one per metric)."""

    def __init__(self, parent, state: AppState, controller: AppController):
        super().__init__(parent, padding=10)
        self.appState = state
        self.controller = controller
        # Guard: only re-render when the result object changes (D-022).
        self._last_result = _UNSET

        self.appState.subscribe(self._on_state_changed)
        self._build_ui()
        self._render()

    def _build_ui(self):
        ttk.Label(self, text="Topic Quality Metrics", font=("Helvetica", 12, "bold")).pack(pady=10)
        self.figure = Figure(figsize=(6, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack(fill=BOTH, expand=YES)

    def _on_state_changed(self, state: AppState):
        self._render()

    def _render(self):
        result = self.appState.current_result
        if result is self._last_result:
            return
        self._last_result = result
        metrics = result.quality_metrics if result else None
        self._draw_gauges(metrics)

    def _draw_gauges(self, metrics: Optional[Dict[str, Optional[float]]]):
        self.figure.clear()
        if not metrics:
            ax = self.figure.add_subplot(111)
            ax.text(0.5, 0.5, "No metrics available", ha="center", va="center", fontsize=12)
            ax.axis("off")
            self.canvas.draw()
            return

        for i, (key, (label, (vmin, vmax), color)) in enumerate(_METRIC_CONFIG.items()):
            ax = self.figure.add_subplot(2, 2, i + 1)
            self._draw_gauge(ax, metrics.get(key), label, vmin, vmax, color)
        self.figure.tight_layout()
        self.canvas.draw()

    def _draw_gauge(self, ax, value, label, vmin, vmax, color):
        """Draw a single donut gauge on the given axes."""
        # Background ring (full range)
        ax.add_patch(Wedge((0.5, 0.5), 0.4, 0, 360, width=0.12, facecolor="#e0e0e0", edgecolor="none"))
        if value is not None:
            frac = max(0.0, min(1.0, (value - vmin) / (vmax - vmin)))
            ax.add_patch(
                Wedge((0.5, 0.5), 0.4, 0, frac * 360, width=0.12, facecolor=color, edgecolor="none")
            )
            ax.text(0.5, 0.5, f"{value:.3f}", ha="center", va="center", fontsize=13, fontweight="bold")
        else:
            ax.text(0.5, 0.5, "N/A", ha="center", va="center", fontsize=13, color="#888888")
        ax.text(0.5, 0.06, label, ha="center", va="center", fontsize=9)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect("equal")
        ax.axis("off")
