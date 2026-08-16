import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from abc import ABC, abstractmethod
from app.models.app_state import AppState
from app.controllers.app_controller import AppController

class BaseHyperparamSection(ttk.Frame, ABC):
    """
    Abstract base class for hyperparameter sections.
    Provides common access to AppState and AppController.
    """
    def __init__(self, parent, state: AppState, controller: AppController):
        super().__init__(parent, padding=10)
        self.appState: AppState = state
        self.controller = controller

    def _bind_param(self, var, param_name: str):
        """Bind a tkinter variable to a state parameter for real-time updates."""
        var.trace_add("write", lambda *args: self.controller.on_param_changed(param_name, var.get()))

    @abstractmethod
    def get_params(self) -> dict:
        """Return the current parameter values as a dictionary."""
        pass
