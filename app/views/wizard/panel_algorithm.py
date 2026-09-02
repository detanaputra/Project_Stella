import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog
from app.models.app_state import AppState
from app.controllers.app_controller import AppController

class AlgorithmPanel(ttk.Frame):
    """Step 1: Algorithm selection and file loading."""

    def __init__(self, parent, state: AppState, controller: AppController):
        super().__init__(parent, padding=20)
        self.appState: AppState = state
        self.controller = controller

        self._build_ui()

    def _build_ui(self):
        # Title
        ttk.Label(self, text="Algorithm & Data Selection", font=("Helvetica", 14, "bold")).pack(pady=(0, 20))

        # Algorithm Selection
        algo_frame = ttk.Frame(self)
        algo_frame.pack(fill=X, pady=10)
        ttk.Label(algo_frame, text="Select Algorithm:", width=20).pack(side=LEFT)
        self.algo_var = ttk.StringVar(value=self.appState.selected_algorithm)
        self.algo_combo = ttk.Combobox(
            algo_frame,
            textvariable=self.algo_var,
            values=["BERTopic"],
            state="readonly"
        )
        self.algo_combo.pack(side=LEFT, fill=X, expand=YES)
        self.algo_combo.bind("<<ComboboxSelected>>", self._update_algo)

        # File Selection
        file_frame = ttk.Frame(self)
        file_frame.pack(fill=X, pady=10)
        ttk.Label(file_frame, text="Data File:", width=20).pack(side=LEFT)
        self.file_var = ttk.StringVar(value=self.appState.selected_file_path or "")
        self.file_entry = ttk.Entry(file_frame, textvariable=self.file_var)
        self.file_entry.pack(side=LEFT, fill=X, expand=YES, padx=(0, 10))
        ttk.Button(file_frame, text="Browse", command=self._browse_file).pack(side=LEFT)

        # Settings Option
        settings_frame = ttk.Frame(self)
        settings_frame.pack(fill=X, pady=20)
        ttk.Label(settings_frame, text="Parameterization:", width=20).pack(side=LEFT)

        self.settings_var = ttk.StringVar(value="default")
        ttk.Radiobutton(settings_frame, text="Default Settings", variable=self.settings_var, value="default").pack(side=LEFT, padx=10)
        ttk.Radiobutton(settings_frame, text="Custom Settings", variable=self.settings_var, value="custom").pack(side=LEFT, padx=10)

    def _update_algo(self, event=None):
        # Views must not mutate AppState directly — the controller runs the logic.
        self.controller.on_algorithm_changed(self.algo_var.get())

    def _browse_file(self):
        path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if path:
            self.file_var.set(path)
            # The controller validates the file and updates state + preview.
            self.controller.on_file_selected(path)

    def get_current_values(self):
        """Returns current panel values to sync with state before moving next."""
        return {
            "algorithm": self.algo_var.get(),
            "file_path": self.file_var.get(),
            "settings_mode": self.settings_var.get()
        }
