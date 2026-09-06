"""Shared window-positioning helpers for top-level dialogs (v0.4.0, WP3)."""


def center_on_parent(window, parent, width: int, height: int) -> None:
    """Position ``window`` centered on ``parent``, sized width x height.

    Call while the window is withdrawn (hidden) so it never flashes at the
    default position; then ``deiconify()`` to show it centered.
    """
    parent.update_idletasks()
    x = parent.winfo_rootx() + (parent.winfo_width() - width) // 2
    y = parent.winfo_rooty() + (parent.winfo_height() - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")
