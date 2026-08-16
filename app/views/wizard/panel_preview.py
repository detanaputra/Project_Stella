import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import pandas as pd
from app.models.app_state import AppState
from app.controllers.app_controller import AppController

class PreviewPanel(ttk.Frame):
    """Step 2: Data preview displaying the head of the loaded file."""

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
            columns=(),
            show="headings",
            bootstyle="info"
        )

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

    def refresh_preview(self):
        """Load data from state and populate the Treeview."""
        # Clear existing
        self.tree.delete(*self.tree.get_children())

        file_path = self.appState.selected_file_path
        if not file_path:
            ttk.Label(self, text="No file selected. Please go back and select a file.").pack()
            return

        try:
            # Load head of the file
            if file_path.lower().endswith('.csv'):
                df = pd.read_csv(file_path, nrows=10)
            else:
                # For txt files, we treat each line as a record in a single column
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = [f.readline().strip() for _ in range(10)]
                df = pd.DataFrame(lines, columns=["Text Content"])

            # Setup columns
            self.tree["columns"] = list(df.columns)
            for col in df.columns:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=150)

            # Insert data
            for idx, row in df.iterrows():
                self.tree.insert("", END, values=list(row))

        except Exception as e:
            ttk.Label(self, text=f"Error loading preview: {str(e)}", bootstyle="danger").pack()
