import tkinter as tk
from app.views.menus.base_menu import BaseMenu

class EditMenu(BaseMenu):
    """Handles the 'Edit' menu and its corresponding commands."""

    def build(self, menubar: tk.Menu) -> tk.Menu:
        # Create the Edit menu
        edit_menu = tk.Menu(menubar, tearoff=False)

        # Placeholder commands
        edit_menu.add_command(label="Undo", command=self._on_undo)
        edit_menu.add_command(label="Redo", command=self._on_redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=lambda: print("Edit: Cut"))
        edit_menu.add_command(label="Copy", command=lambda: print("Edit: Copy"))
        edit_menu.add_command(label="Paste", command=lambda: print("Edit: Paste"))

        return edit_menu

    def _on_undo(self) -> None:
        print("Menu Action: Undo")

    def _on_redo(self) -> None:
        print("Menu Action: Redo")
