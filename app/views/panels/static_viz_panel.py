"""Static visualisation tab: a matplotlib chart of one BERTopic visualization.

Renders lazily — the chart is generated the first time the tab is viewed
(v0.3.0, WP1), not when the result appears. Follows the cheap-subscriber
discipline (D-022): it only re-renders when the result object changes.
"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from app.models.app_state import AppState
from app.controllers.app_controller import AppController


# Sentinel distinct from None (D-014).
_UNSET = object()


class StaticVizPanel(ttk.Frame):
    """A tab showing a static matplotlib chart of one BERTopic visualization,
    with an "Open interactive" button that opens the Plotly HTML in the browser."""

    def __init__(self, parent, state: AppState, controller: AppController,
                 viz_name: str, title: str):
        super().__init__(parent, padding=10)
        self.appState = state
        self.controller = controller
        self.viz_name = viz_name
        self.title = title
        self._last_result = _UNSET
        self._rendered_for = _UNSET  # which result the chart was generated for

        self._build_ui()
        self.appState.subscribe(self._on_state_changed)
        self._show_placeholder()

    def _build_ui(self):
        header = ttk.Frame(self)
        header.pack(fill=X, pady=(0, 8))
        ttk.Label(header, text=self.title, font=("Helvetica", 12, "bold")).pack(side=LEFT)
        ttk.Button(header, text="Open interactive", bootstyle="info-outline",
                   command=self._on_open_interactive).pack(side=RIGHT)

        self.figure = Figure(figsize=(7, 5), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack(fill=BOTH, expand=YES)

    def _on_state_changed(self, state: AppState):
        result = self.appState.current_result
        if result is self._last_result:
            return
        self._last_result = result
        self._rendered_for = _UNSET  # invalidate the generated chart
        self._show_placeholder()

    def ensure_rendered(self):
        """Generate the static chart on first view (lazy)."""
        result = self.appState.current_result
        if result is None or result is self._rendered_for:
            return
        self._rendered_for = result
        self._draw()

    def _on_open_interactive(self):
        self.controller.open_interactive_viz(self.viz_name)

    def _show_placeholder(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.text(0.5, 0.5, "Generating chart on first view…", ha="center", va="center", fontsize=11)
        ax.axis("off")
        self.canvas.draw()

    def _draw(self):
        self.figure.clear()
        ok = self.controller.render_static_chart(self.viz_name, self.figure)
        if not ok:
            ax = self.figure.add_subplot(111)
            ax.text(0.5, 0.5, "Could not render chart", ha="center", va="center", fontsize=11)
            ax.axis("off")
        self.canvas.draw()
