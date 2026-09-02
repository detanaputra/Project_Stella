import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from app.models.app_state import AppState
from app.controllers.app_controller import AppController

class PreviewPanel(ttk.Frame):
    """Step 2: Data preview displaying the head of the loaded file.

    No file I/O in views: the preview comes from AppState.file_preview, which
    the controller populated through DataLoader.load_preview.
    """

    def __init__(self, parent, state: AppState, controller: AppController):
        super().__init__(parent, padding=20)
        self.appState: AppState = state
        self.controller = controller

        self._build_ui()

    def _build_ui(self):
        ttk.Label(self, text="Data Preview", font=("Helvetica", 14, "bold")).pack(pady=(0, 10))
        ttk.Label(self, text="First 10 records from the selected file:").pack(pady=(0, 10))

        # Treeview for table display
        self.table_frame = ttk.Frame(self)
        self.table_frame.pack(fill=BOTH, expand=YES)

        self.tree = ttk.Treeview(
            self.table_frame,
            columns=("Text Content",),
            show="headings",
            bootstyle="info"
        )
        self.tree.heading("Text Content", text="Text Content")
        self.tree.column("Text Content", width=400)

        # Add vertical and horizontal scrollbars
        self.vsb = ttk.Scrollbar(self.table_frame, orient=VERTICAL, command=self.tree.yview)
        self.hsb = ttk.Scrollbar(self.table_frame, orient=HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)

        # Layout tree and scrollbars
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.vsb.grid(row=0, column=1, sticky="ns")
        self.hsb.grid(row=1, column=0, sticky="ew")
        self.table_frame.grid_columnconfigure(0, weight=1)
        self.table_frame.grid_rowconfigure(0, weight=1)

        # Status line (reused, so repeated refreshes do not stack labels)
        self.status_lbl = ttk.Label(self, text="", bootstyle="secondary")
        self.status_lbl.pack(pady=(8, 0))

    def _set_status(self, text: str):
        self.status_lbl.config(text=text)

    def refresh_preview(self):
        """Populate the Treeview from state — no direct file reading."""
        self.tree.delete(*self.tree.get_children())
        self._set_status("")

        file_path = self.appState.selected_file_path
        if not file_path:
            self._set_status("No file selected. Please go back and select a file.")
            return

        # No direct file I/O in views: ensure the preview is loaded through the
        # controller (which delegates to DataLoader), then render what state holds.
        if not self.appState.file_preview:
            self.controller.on_file_selected(file_path)

        preview = self.appState.file_preview or []
        if not preview:
            self._set_status("No preview available for this file.")
            return

        for text in preview:
            self.tree.insert("", END, values=(text,))
