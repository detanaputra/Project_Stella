import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog
from app.models.app_state import AppState
from app.controllers.app_controller import AppController

class InputPanel(ttk.Frame):
    """Panel for file selection and data preview."""

    def __init__(self, parent, state: AppState, controller: AppController):
        super().__init__(parent)
        self.appState: AppState = state
        self.controller = controller

        self.appState.subscribe(self._on_state_changed)
        self._build_ui()
        self._render()

    def _build_ui(self):
        self.frame = ttk.Frame(self)
        self.frame.pack(fill=X, pady=5)

        self.lbl_title = ttk.Label(self.frame, text="1. Load Data", font=("Helvetica", 12, "bold"))
        self.lbl_title.pack(side=LEFT, padx=5)

        self.btn_browse = ttk.Button(
            self.frame,
            text="Select CSV/TXT File",
            bootstyle="outline-primary",
            command=self._on_browse_clicked
        )
        self.btn_browse.pack(side=LEFT, padx=10)

        self.lbl_file = ttk.Label(self.frame, text="No file selected", font=("Helvetica", 10, "italic"))
        self.lbl_file.pack(side=LEFT, padx=10)

        # Preview area
        self.preview_text = ttk.Text(self, height=5, font=("Consolas", 9))
        self.preview_text.pack(fill=X, pady=5)
        self.preview_text.config(state=DISABLED)

    def _on_browse_clicked(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if file_path:
            self.controller.on_file_selected(file_path)

    def _on_state_changed(self, state: AppState):
        self._render()

    def _render(self):
        # Update file label
        if self.appState.selected_file_path:
            self.lbl_file.config(text=f"Selected: {self.appState.selected_file_path}")
        else:
            self.lbl_file.config(text="No file selected")

        # Update preview
        self.preview_text.config(state=NORMAL)
        self.preview_text.delete("1.0", END)
        if self.appState.file_preview:
            preview_content = "\n".join(self.appState.file_preview)
            self.preview_text.insert(END, preview_content)
        self.preview_text.config(state=DISABLED)
