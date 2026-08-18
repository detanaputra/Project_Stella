import tkinter as tk
from app.views.menus.base_menu import BaseMenu

class EditMenu(BaseMenu):
    """Handles the 'Edit' menu and its corresponding commands.

    Commands forward standard Tk editing events to the currently focused
    widget (parameter spinboxes, the file preview, etc.). If the focused
    widget has no binding for the event it is silently ignored — no print
    placeholders, no fake actions (audit L1).
    """

    def build(self, menubar: tk.Menu) -> tk.Menu:
        # Create the Edit menu
        edit_menu = tk.Menu(menubar, tearoff=False)

        edit_menu.add_command(label="Undo", command=self._on_undo)
        edit_menu.add_command(label="Redo", command=self._on_redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=lambda: self._generate('<<Cut>>'))
        edit_menu.add_command(label="Copy", command=lambda: self._generate('<<Copy>>'))
        edit_menu.add_command(label="Paste", command=lambda: self._generate('<<Paste>>'))

        return edit_menu

    def _on_undo(self) -> None:
        self._generate('<<Undo>>')

    def _on_redo(self) -> None:
        self._generate('<<Redo>>')

    def _generate(self, event_name: str) -> None:
        """Forward an editing event to the currently focused widget."""
        widget = self.root.focus_get()
        if widget is not None:
            widget.event_generate(event_name)
