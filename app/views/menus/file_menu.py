import tkinter as tk
from tkinter import filedialog
from app.views.menus.base_menu import BaseMenu
from app.views.wizard.wizard_main import TopicModelWizard

class FileMenu(BaseMenu):
    """Handles the 'File' menu and its corresponding commands."""

    def build(self, menubar: tk.Menu) -> tk.Menu:
        # Create the File menu
        file_menu = tk.Menu(menubar, tearoff=False)

        # Add commands
        file_menu.add_command(label="New Project...", command=self._on_new)
        file_menu.add_command(label="Save Project", command=self._on_save)
        file_menu.add_command(label="Load Project", command=self._on_load)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        return file_menu

    def _on_new(self) -> None:
        """Launch the Topic Model Creation Wizard."""
        # We need the analysis controller as well for the 'Train' action
        # The MenuManager has the AppController, but we need to get the AnalysisController
        # from the MainWindow (self.root)
        from app.views.main_window import MainWindow
        if isinstance(self.root, MainWindow):
            wizard = TopicModelWizard(
                self.root,
                self.root.appState,
                self.root.app_controller,
                self.root.analysis_controller
            )
            wizard.mainloop()
        else:
            print("Error: Root is not a MainWindow")

    def _on_save(self) -> None:
        """Prompt for file path and save current project state."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".stella",
            filetypes=[("Stella Project", "*.stella")],
            title="Save Project"
        )
        if file_path:
            self.controller.save_project(file_path)

    def _on_load(self) -> None:
        """Prompt for file path and load project state."""
        file_path = filedialog.askopenfilename(
            filetypes=[("Stella Project", "*.stella")],
            title="Load Project"
        )
        if file_path:
            self.controller.load_project(file_path)
