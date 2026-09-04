"""Static visualisation tab: displays a pre-generated static chart.

The chart is generated once by the pipeline (after training, in the
background) and saved as a PNG; this panel just displays it (v0.3.0, WP1).
The "Open interactive" button opens the pre-generated offline HTML in the
browser. Follows the cheap-subscriber discipline (D-022): it only re-renders
when the result object changes.
"""

import os

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk

from app.models.app_state import AppState
from app.controllers.app_controller import AppController


# Sentinel distinct from None (D-014).
_UNSET = object()


class StaticVizPanel(ttk.Frame):
    """A tab showing a pre-generated static chart of one BERTopic visualization,
    with an "Open interactive" button that opens the Plotly HTML in the browser."""

    def __init__(self, parent, state: AppState, controller: AppController,
                 viz_name: str, title: str):
        super().__init__(parent, padding=10)
        self.appState = state
        self.controller = controller
        self.viz_name = viz_name
        self.title = title
        self._last_result = _UNSET
        self._photo = None  # keep a reference so the image is not GC'd

        self._build_ui()
        self.appState.subscribe(self._on_state_changed)
        self._render()

    def _build_ui(self):
        header = ttk.Frame(self)
        header.pack(fill=X, pady=(0, 8))
        ttk.Label(header, text=self.title, font=("Helvetica", 12, "bold")).pack(side=LEFT)
        ttk.Button(header, text="Open interactive", bootstyle="info-outline",
                   command=self._on_open_interactive).pack(side=RIGHT)

        self.image_label = ttk.Label(self)
        self.image_label.pack(fill=BOTH, expand=YES)

    def _on_state_changed(self, state: AppState):
        self._render()

    def _on_open_interactive(self):
        self.controller.open_interactive_viz(self.viz_name)

    def _render(self):
        result = self.appState.current_result
        if result is self._last_result:
            return
        self._last_result = result
        path = self.controller.get_static_chart_path(self.viz_name)
        if path and os.path.exists(path):
            try:
                img = Image.open(path)
                img.thumbnail((700, 500))
                self._photo = ImageTk.PhotoImage(img)
                self.image_label.config(image=self._photo, text="")
            except Exception:
                self._photo = None
                self.image_label.config(image="", text="Could not load chart")
        else:
            self._photo = None
            self.image_label.config(image="", text="No chart available")
