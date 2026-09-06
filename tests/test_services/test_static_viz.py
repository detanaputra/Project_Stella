"""Tests for the static visualisation converter."""

import os

import plotly.graph_objects as go

from app.models.services.static_viz import plotly_fig_to_mpl, save_static_charts


def test_plotly_fig_to_mpl_scatter():
    fig = go.Figure(go.Scatter(x=[1, 2, 3], y=[4, 5, 6], mode="markers"))
    mpl_fig = plotly_fig_to_mpl(fig.to_dict(), viz_name="topics")
    assert mpl_fig is not None
    assert len(mpl_fig.axes) >= 1


def test_plotly_fig_to_mpl_heatmap():
    fig = go.Figure(go.Heatmap(z=[[1, 2], [3, 4]]))
    mpl_fig = plotly_fig_to_mpl(fig.to_dict(), viz_name="heatmap")
    assert mpl_fig is not None


def test_save_static_charts(tmp_path, trained_result):
    model = trained_result.metadata["model"]
    paths = save_static_charts(model, str(tmp_path))
    assert len(paths) >= 1
    for p in paths.values():
        assert os.path.exists(p)
