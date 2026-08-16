import tkinter as tk
from app.controllers.app_controller import AppController
from app.views.menus.file_menu import FileMenu
from app.views.menus.edit_menu import EditMenu
from app.views.menus.view_menu import ViewMenu
from app.views.menus.window_menu import WindowMenu

class MenuManager:
    """
    Orchestrates the application's top-level menu bar by assembling
    individual menu parent components.
    """
    def __init__(self, root, controller: AppController):
        self.root = root
        self.controller = controller

    def build_menu(self) -> None:
        """
        Constructs the menu bar by calling build methods on individual menu parents
        and attaching the result to the root window.
        """
        # Create the main menu bar
        menubar = tk.Menu(self.root)

        # Instantiate menu parents
        menus = {
            "File": FileMenu(self.root, self.controller),
            "Edit": EditMenu(self.root, self.controller),
            "View": ViewMenu(self.root, self.controller),
            "Window": WindowMenu(self.root, self.controller),
        }

        # Build and add each menu to the menubar
        for label, menu_parent in menus.items():
            menu_obj = menu_parent.build(menubar)
            menubar.add_cascade(label=label, menu=menu_obj)

        # Configure the root window to use this menubar
        self.root.config(menu=menubar)
