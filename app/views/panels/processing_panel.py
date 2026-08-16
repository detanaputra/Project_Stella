import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from app.models.app_state import AppState
from app.controllers.analysis_controller import AnalysisController

class ProcessingPanel(ttk.Frame):
    """Panel for training progress and status messages."""

    def __init__(self, parent, state: AppState, controller: AnalysisController):
        super().__init__(parent)
        self.appState: AppState = state
        self.controller = controller

        self.appState.subscribe(self._on_state_changed)
        self._build_ui()
        self._render()

    def _build_ui(self):
        self.frame = ttk.Frame(self)
        self.frame.pack(fill=X, pady=5)

        self.lbl_title = ttk.Label(self.frame, text="3. Run Analysis", font=("Helvetica", 12, "bold"))
        self.lbl_title.pack(side=LEFT, padx=5)

        self.btn_run = ttk.Button(
            self.frame,
            text="Start Training",
            bootstyle="success",
            command=self.controller.run_analysis
        )
        self.btn_run.pack(side=LEFT, padx=10)

        # Progress container
        self.progress_frame = ttk.Frame(self)
        self.progress_frame.pack(fill=X, pady=10)

        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            bootstyle="success-striped",
            mode="determinate"
        )
        self.progress_bar.pack(fill=X, padx=5)

        self.lbl_status = ttk.Label(self.progress_frame, text="Ready", font=("Helvetica", 10))
        self.lbl_status.pack(pady=5)

    def _on_state_changed(self, state: AppState):
        self._render()

    def _render(self):
        # Update button state
        can_run = (
            self.appState.selected_file_path is not None and
            not self.appState.analysis_in_progress
        )
        self.btn_run.config(state="normal" if can_run else "disabled")

        # Update progress bar
        if self.appState.analysis_in_progress:
            try:
                percent = int(self.appState.analysis_progress.replace('%', ''))
                self.progress_bar['value'] = percent
            except ValueError:
                self.progress_bar['value'] = 0
        else:
            self.progress_bar['value'] = 0 if not self.appState.current_result else 100

        # Update status text
        self.lbl_status.config(text=self.appState.analysis_status)
