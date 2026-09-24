import threading
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox
from app.models.app_state import AppState
from app.controllers.app_controller import AppController

class ExportPanel(ttk.Frame):
    """Panel for exporting results: CSV, JSON, methodology report, and
    interactive browser visualizations (audit M4)."""

    def __init__(self, parent, state: AppState, controller: AppController):
        super().__init__(parent, padding=20)
        self.appState: AppState = state
        self.controller: AppController = controller
        self._build_ui()

    def _build_ui(self):
        desc_frame = ttk.Frame(self)
        desc_frame.pack(anchor=W)
        ttk.Label(desc_frame, text="Export Results", font=("Helvetica", 14, "bold")).pack(anchor=W, pady=(0, 8))
        ttk.Label(
            desc_frame,
            text="Export the current analysis for sharing, publication, and reproducibility.",
            wraplength=250,
            justify=LEFT,
        ).pack(anchor=W, pady=(0, 24))

        btn_frame = ttk.Frame(self)
        btn_frame.pack(anchor=W)

        ttk.Button(btn_frame, text="Export Topics", bootstyle="outline-secondary", command=self._on_export_csv_topics).pack(fill=X, pady=5)
        ttk.Button(btn_frame, text="Export Document Assignments", bootstyle="outline-secondary", command=self._on_export_csv_assignments).pack(fill=X, pady=5)
        ttk.Button(btn_frame, text="Export Model Record (JSON)", bootstyle="outline-secondary", command=self._on_export_json).pack(fill=X, pady=5)
        ttk.Button(btn_frame, text="Export Methodology Report", bootstyle="outline-secondary", command=self._on_export_report).pack(fill=X, pady=5)
        self._viz_btn = ttk.Button(
            btn_frame,
            text="Open Visualizations in Browser",
            bootstyle="info",
            command=self._on_export_visualizations,
        )
        self._viz_btn.pack(fill=X, pady=5)

    def _require_result(self) -> bool:
        if not self.appState.current_result:
            messagebox.showwarning(
                "No Analysis",
                "Please run an analysis first before exporting.",
                parent=self,
            )
            return False
        return True

    def _on_export_csv_topics(self):
        if not self._require_result():
            return
        path = filedialog.asksaveasfilename(
            parent=self, defaultextension=".csv", filetypes=[("CSV files", "*.csv")]
        )
        if path:
            self.controller.export_csv_topics(path)

    def _on_export_csv_assignments(self):
        if not self._require_result():
            return
        path = filedialog.asksaveasfilename(
            parent=self, defaultextension=".csv", filetypes=[("CSV files", "*.csv")]
        )
        if path:
            self.controller.export_csv_assignments(path)

    def _on_export_json(self):
        if not self._require_result():
            return
        path = filedialog.asksaveasfilename(
            parent=self, defaultextension=".json", filetypes=[("JSON files", "*.json")]
        )
        if path:
            self.controller.export_json(path)

    def _on_export_report(self):
        if not self._require_result():
            return
        path = filedialog.asksaveasfilename(
            parent=self, defaultextension=".md", filetypes=[("Markdown files", "*.md")]
        )
        if path:
            self.controller.export_methodology_report(path)

    def _on_export_visualizations(self):
        """Generate the BERTopic plots off the main thread so the UI does not
        freeze for the few seconds the figures take to build (audit M1/M4)."""
        if not self._require_result():
            return
        self._viz_btn.config(state="disabled", text="Generating visualizations...")

        def worker():
            try:
                message = self.controller.export_visualizations()
            except Exception as e:  # surface generation errors instead of a silent no-op
                message = str(e)
            self.appState.call_on_main(lambda: self._finish_viz(message))

        threading.Thread(target=worker, daemon=True).start()

    def _finish_viz(self, message: str):
        self._viz_btn.config(state="normal", text="Open Visualizations in Browser")
        if message:
            messagebox.showerror("Export Failed", message, parent=self)
        else:
            messagebox.showinfo(
                "Export Complete",
                "Visualizations generated and opened in your browser.",
                parent=self,
            )
