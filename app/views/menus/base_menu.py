import tkinter as tk
from abc import ABC, abstractmethod
from app.controllers.app_controller import AppController

class BaseMenu(ABC):
    """
    Abstract base class for menu parents.
    Provides common access to the root window and the application controller.
    """
    def __init__(self, root, controller: AppController):
        self.root = root
        self.controller = controller

    @abstractmethod
    def build(self, menubar: tk.Menu) -> tk.Menu:
        """
        Build the specific menu and return it.

        Args:
            menubar: The main menu bar to which this menu will be attached.

        Returns:
            A configured tk.Menu object.
        """
        pass
