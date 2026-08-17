import tkinter as tk
from app.views.menus.base_menu import BaseMenu

class ViewMenu(BaseMenu):
    """Handles the 'View' menu and its corresponding commands."""

    def build(self, menubar: tk.Menu) -> tk.Menu:
        # Create the View menu
        view_menu = tk.Menu(menubar, tearoff=False)

        # Placeholder commands
        view_menu.add_command(label="Zoom In", command=self._on_zoom_in)
        view_menu.add_command(label="Zoom Out", command=self._on_zoom_out)
        view_menu.add_separator()

        return view_menu

    def _on_zoom_in(self) -> None:
        print("Menu Action: Zoom In")

    def _on_zoom_out(self) -> None:
        print("Menu Action: Zoom Out")
