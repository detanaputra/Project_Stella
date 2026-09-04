"""Convert BERTopic's Plotly visualizations to static matplotlib figures.

BERTopic's ``visualize_*`` methods return Plotly figures only. ``fig.to_dict()``
exposes the rendered data (coordinates, sizes, labels, matrices) as a plain
dict, which this module re-plots with matplotlib for the in-app static tabs
(v0.3.0, WP1). The interactive Plotly HTML remains available via the
"Open interactive" button.

Design (settled): clean matplotlib defaults (not pixel-matched to Plotly); the
hierarchy dendrogram uses a simple line representation for the MVP.
"""

import re
from typing import Any, Dict, List, Optional

import numpy as np
from matplotlib.figure import Figure


def plotly_fig_to_mpl(fig_dict: Dict[str, Any], figure: Optional[Figure] = None) -> Figure:
    """Render a Plotly figure dict (from ``fig.to_dict()``) as a matplotlib Figure.

    Dispatches on each trace's ``type``. Traces that reference distinct axes
    (BERTopic's barchart uses one subplot per topic) are drawn on subplots;
    everything else shares a single axes. Draws onto ``figure`` when given,
    otherwise creates one.
    """
    data = fig_dict.get("data", [])
    layout = fig_dict.get("layout", {})

    if figure is None:
        figure = Figure(figsize=(8, 6), dpi=100)
    figure.clear()

    # Group traces by their xaxis reference: 'x'/'x' -> 0, 'x2' -> 1, ...
    groups: Dict[int, List[Dict[str, Any]]] = {}
    for trace in data:
        xref = trace.get("xaxis", "x")
        idx = 0 if xref in ("x", "") else int(xref[1:]) - 1
        groups.setdefault(idx, []).append(trace)

    if len(groups) <= 1:
        ax = figure.add_subplot(111)
        for trace in data:
            _render_trace(ax, trace)
    else:
        n = len(groups)
        cols = 2 if n > 1 else 1
        rows = int(np.ceil(n / cols))
        for idx, traces in sorted(groups.items()):
            ax = figure.add_subplot(rows, cols, idx + 1)
            for trace in traces:
                _render_trace(ax, trace)
            title = _axis_title(layout, idx)
            if title:
                ax.set_title(title, fontsize=9)

    title = _strip_html(layout.get("title", {}).get("text", ""))
    if title:
        figure.suptitle(title, fontsize=11)
        figure.tight_layout(rect=[0, 0, 1, 0.95])
    else:
        figure.tight_layout()
    return figure


def static_chart(model, viz_name: str, figure: Optional[Figure] = None) -> Figure:
    """Generate a static matplotlib chart for a BERTopic visualization by name.

    Args:
        model: the trained BERTopic model (from ``TopicResult.metadata``).
        viz_name: one of "topics", "heatmap", "barchart", "hierarchy", "term_rank".
        figure: optional matplotlib Figure to draw onto.

    Raises:
        ValueError: if the model has no ``visualize_<viz_name>`` method.
    """
    method = getattr(model, f"visualize_{viz_name}", None)
    if method is None:
        raise ValueError(f"visualize_{viz_name} not available on the model")
    plotly_fig = method()
    return plotly_fig_to_mpl(plotly_fig.to_dict(), figure=figure)


# --- trace renderers -------------------------------------------------------


def _render_trace(ax, trace: Dict[str, Any]) -> None:
    t = trace.get("type")
    if t == "scatter":
        _render_scatter(ax, trace)
    elif t == "heatmap":
        _render_heatmap(ax, trace)
    elif t == "bar":
        _render_bar(ax, trace)
    # Other trace types (annotation overlays, etc.) are ignored for the MVP.


def _render_scatter(ax, trace: Dict[str, Any]) -> None:
    x = np.asarray(trace.get("x", []), dtype=float)
    y = np.asarray(trace.get("y", []), dtype=float)
    if x.size == 0 or y.size == 0:
        return
    mode = trace.get("mode", "markers")
    if "lines" in mode:
        # Line segments (e.g. the hierarchy dendrogram, term_rank) — simple
        # representation for the MVP.
        ax.plot(x, y, color=_trace_color(trace), linewidth=1.5)
        return
    sizes = _marker_sizes(trace)
    ax.scatter(x, y, s=sizes, color=_trace_color(trace), alpha=0.85,
               edgecolors="white", linewidths=0.5)
    labels = _trace_labels(trace)
    if labels is not None:
        for xi, yi, lab in zip(x, y, labels):
            ax.annotate(lab, (xi, yi), fontsize=8, ha="center", va="bottom")


def _render_heatmap(ax, trace: Dict[str, Any]) -> None:
    z = np.asarray(trace.get("z"))
    if z.size == 0:
        return
    im = ax.imshow(z, cmap="viridis", aspect="auto")
    x = trace.get("x")
    y = trace.get("y")
    if x:
        ax.set_xticks(range(len(x)))
        ax.set_xticklabels([str(v) for v in x], rotation=45, ha="right", fontsize=8)
    if y:
        ax.set_yticks(range(len(y)))
        ax.set_yticklabels([str(v) for v in y], fontsize=8)
    ax.figure.colorbar(im, ax=ax)


def _render_bar(ax, trace: Dict[str, Any]) -> None:
    x = trace.get("x")
    y = trace.get("y")
    if x is None or y is None:
        return
    if trace.get("orientation") == "h":
        # BERTopic's barchart: x = weights, y = term labels.
        ax.barh([str(v) for v in y], x, color=_trace_color(trace))
    else:
        ax.bar([str(v) for v in x], y, color=_trace_color(trace))


# --- helpers ---------------------------------------------------------------


def _trace_color(trace: Dict[str, Any]) -> str:
    marker = trace.get("marker", {})
    color = marker.get("color")
    if isinstance(color, str):
        return color
    return "#1f77b4"


def _marker_sizes(trace: Dict[str, Any]) -> Any:
    marker = trace.get("marker", {})
    sizes = marker.get("size")
    if sizes is None:
        return 60
    arr = np.asarray(sizes, dtype=float)
    if arr.size == 0 or arr.max() <= 0:
        return 60
    # Plotly uses area mode with sizeref; scale to matplotlib points^2 so the
    # largest topic stays readable.
    return (arr / arr.max()) * 400 + 40


def _trace_labels(trace: Dict[str, Any]) -> Optional[List[str]]:
    customdata = trace.get("customdata")
    if customdata is not None:
        arr = np.asarray(customdata)
        if arr.ndim == 2 and arr.shape[1] >= 2:
            return [str(r[1]) for r in arr]
    text = trace.get("text")
    if text is not None:
        return [str(t) for t in text]
    return None


def _axis_title(layout: Dict[str, Any], idx: int) -> str:
    key = "xaxis" if idx == 0 else f"xaxis{idx + 1}"
    return _strip_html(layout.get(key, {}).get("title", {}).get("text", ""))


def _strip_html(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text) if text else ""
