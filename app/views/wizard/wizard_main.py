import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import Toplevel
from app.models.app_state import AppState
from app.controllers.app_controller import AppController
from app.controllers.analysis_controller import AnalysisController
from app.views.wizard.panel_algorithm import AlgorithmPanel
from app.views.wizard.panel_preview import PreviewPanel
from app.views.wizard.panel_hyperparams import HyperparamPanel
from app.views.wizard.panel_summary import SummaryPanel
from app.views.panels.loading_panel import LoadingPanel
from app.views.window_utils import center_on_parent

class TopicModelWizard(Toplevel):
    """
    Wizard-style interface for creating a new topic model.
    Guides the user through Algorithm selection, Preview, Hyperparameters, and Summary.
    """
    def __init__(self, parent, state: AppState, app_controller: AppController, analysis_controller: AnalysisController):
        super().__init__(parent)
        self.title("Create New Topic Model")
        self.withdraw()  # keep hidden until positioned (v0.4.0, WP3)
        self.resizable(False, False)

        # Modal behavior
        self.transient(parent)

        self.parent = parent
        self.appState: AppState = state
        self.app_controller = app_controller
        self.analysis_controller = analysis_controller
        self.current_step = 0

        self._build_ui()

        # Position centered on the main window, then show (v0.4.0, WP3).
        center_on_parent(self, parent, 700, 500)
        self.deiconify()
        self.grab_set()

        self._update_step()

    def _build_ui(self):
        # 1. Navigation Area (Packed first at the bottom)
        self.nav_frame = ttk.Frame(self, padding=20)
        self.nav_frame.pack(side=BOTTOM, fill=X)

        self.btn_prev = ttk.Button(
            self.nav_frame,
            text="Previous",
            bootstyle="secondary-outline",
            command=self._prev_step
        )
        self.btn_prev.pack(side=LEFT, padx=10)

        self.btn_next = ttk.Button(
            self.nav_frame,
            text="Next",
            bootstyle="primary",
            command=self._next_step
        )
        self.btn_next.pack(side=RIGHT, padx=10)

        # 2. Content Area: Notebook (Takes remaining space)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=BOTH, expand=YES, padx=20, pady=20)

        # Instantiate Panels
        self.panel_algo = AlgorithmPanel(self.notebook, self.appState, self.app_controller)
        self.panel_prev = PreviewPanel(self.notebook, self.appState, self.app_controller)
        self.panel_hyper = HyperparamPanel(self.notebook, self.appState, self.app_controller)
        self.panel_summ = SummaryPanel(self.notebook, self.appState, self.app_controller)

        # Add to notebook
        self.notebook.add(self.panel_algo, text="Step 1")
        self.notebook.add(self.panel_hyper, text="Step 2")
        self.notebook.add(self.panel_prev, text="Step 3")
        self.notebook.add(self.panel_summ, text="Step 4")

    def _update_step(self):
        """Update notebook selection and button labels/states."""
        self.notebook.select(self.current_step)

        # Update Previous button
        self.btn_prev.config(state="normal" if self.current_step > 0 else "disabled")

        # Update Next/Train button
        if self.current_step == 3:
            self.btn_next.config(text="Train", bootstyle="success")
        else:
            self.btn_next.config(text="Next", bootstyle="primary")

        # Refresh current panel if needed
        if self.current_step == 2:
            self.panel_prev.refresh_preview()

        if self.current_step == 3:
            # Sync values from panels to a config dict for the summary
            config = {
                "algorithm": self.panel_algo.algo_var.get(),
                "file_path": self.panel_algo.file_var.get(),
                "settings_mode": self.panel_algo.settings_var.get(),
                "params": self.panel_hyper.get_current_params()
            }
            self.panel_summ.update_summary(config)

    def _next_step(self):
        # no need to go to hyperparameter setting panel if user choose Default Setting
        if self.current_step == 0 and self.panel_algo.get_current_values()["settings_mode"] == "default":
            self.current_step = 2
            self._update_step()
        else:
            if self.current_step < 3:
                self.current_step += 1
                self._update_step()
            else:
                # Final Step: Train
                self._handle_train()

    def _prev_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self._update_step()

    def _handle_train(self):
        """Trigger analysis, show loading panel, and close wizard."""
        # Ensure final values are synced to state THROUGH the controller —
        # views must not mutate AppState directly (architecture rule).
        vals = self.panel_algo.get_current_values()
        self.app_controller.on_file_selected(vals["file_path"])
        self.app_controller.on_algorithm_changed(vals["algorithm"])

        # Sync hyperparameters from the hyperparam panel to state.
        # "Custom Settings" applies the panel values; "Default Settings"
        # resets to the algorithm's defaults so both entry points (wizard and
        # main-window retrain) train with identical parameters (audit H2).
        if vals["settings_mode"] == "custom":
            custom_params = self.panel_hyper.get_current_params()
            self.app_controller.set_params(custom_params)

        # 1. Show Loading Panel via MainWindow
        if hasattr(self.parent, 'show_loading_panel'):
            self.parent.show_loading_panel()

        # 2. Trigger analysis
        self.analysis_controller.run_analysis()

        # 3. Close wizard
        self.destroy()
