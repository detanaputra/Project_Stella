import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog
from app.models.app_state import AppState
from app.controllers.app_controller import AppController
from app.models.topic_result import TopicResult
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ResultsPanel(ttk.Frame):
    """Panel for displaying topic results, stats, and export actions."""

    def __init__(self, parent, state: AppState, controller: AppController):
        super().__init__(parent)
        self.appState: AppState = state
        self.controller = controller

        self.appState.subscribe(self._on_state_changed)
        self._build_ui()
        self._render()

    def _build_ui(self):
        self.frame = ttk.Frame(self)
        self.frame.pack(fill=BOTH, expand=YES, pady=5)

        self.lbl_title = ttk.Label(self.frame, text="4. Results", font=("Helvetica", 12, "bold"))
        self.lbl_title.pack(anchor=W, padx=5)

        # Content area: Split into Top Results and Visuals
        self.content = ttk.Frame(self.frame)
        self.content.pack(fill=BOTH, expand=YES, pady=10)

        # Left: Topics Table
        self.table_frame = ttk.Frame(self.content)
        self.table_frame.pack(side=LEFT, fill=BOTH, expand=YES, padx=5)

        # Right: Summary Plot
        self.plot_frame = ttk.Frame(self.content)
        self.plot_frame.pack(side=RIGHT, fill=BOTH, expand=YES, padx=5)

        # Export buttons
        self.export_frame = ttk.Frame(self.frame)
        self.export_frame.pack(fill=X, pady=10)

        self.btn_csv = ttk.Button(self.export_frame, text="Export CSV", bootstyle="outline-secondary", command=self._on_export_csv)
        self.btn_csv.pack(side=LEFT, padx=5)

        self.btn_report = ttk.Button(self.export_frame, text="Export Methodology Report", bootstyle="outline-secondary", command=self._on_export_report)
        self.btn_report.pack(side=LEFT, padx=5)

    def _on_export_csv(self):
        if not self.appState.current_result: return
        path = filedialog.asksaveasfilename(defaultextension=".csv")
        if path:
            # In a real app, we'd call the exporter service through the controller
            from app.models.services.exporter import Exporter
            Exporter().to_csv(self.appState.current_result, path)

    def _on_export_report(self):
        if not self.appState.current_result: return
        path = filedialog.asksaveasfilename(defaultextension=".md")
        if path:
            from app.models.services.exporter import Exporter
            Exporter().generate_methodology_report(self.appState.current_result, path)

    def _on_state_changed(self, state: AppState):
        self._render()

    def _render(self):
        # Clear existing content
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        if not self.appState.current_result:
            ttk.Label(self.table_frame, text="No results yet. Run analysis to see topics.").pack()
            return

        # 1. Render Topics Table (Simple list for now)
        result = self.appState.current_result
        ttk.Label(self.table_frame, text="Top Topics", font=("Helvetica", 10, "bold")).pack(anchor=W)

        for i, topic in enumerate(result.topics[:10]):
            # Get top 3 words
            sorted_words = sorted(topic.items(), key=lambda x: x[1], reverse=True)[:3]
            words_str = ", ".join([f"{w} ({v:.2f})" for w, v in sorted_words])
            ttk.Label(self.table_frame, text=f"Topic {i}: {words_str}").pack(anchor=W, pady=2)

        # 2. Render Summary Plot
        self._render_summary_plot(result)

    def _render_summary_plot(self, result: TopicResult):
        """Embeds a simple matplotlib bar chart of topic prevalence."""
        # Simulating prevalence: in real BERTopic, we'd count docs per topic
        # For this MVP, we'll generate a dummy distribution based on doc_topics
        from collections import Counter

        # Count primary topic for each doc
        primary_topics = []
        for dt in result.doc_topics:
            if dt:
                primary_topics.append(max(dt, key=dt.get))

        counts = Counter(primary_topics)
        sorted_topics = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:10]

        if not sorted_topics: return

        labels, values = zip(*sorted_topics)

        fig, ax = plt.subplots(figsize=(4, 3), dpi=80)
        ax.bar([str(l) for l in labels], values, color='skyblue')
        ax.set_title("Topic Prevalence")
        ax.set_xlabel("Topic ID")
        ax.set_ylabel("Doc Count")
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()
