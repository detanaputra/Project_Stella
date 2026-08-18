import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import Scrollbar
from app.models.app_state import AppState
from app.controllers.app_controller import AppController
from app.models.topic_result import TopicResult

class SummaryPanel(ttk.Frame):
    """Panel for displaying summary information and key metrics."""

    def __init__(self, parent, state: AppState, controller: AppController):
        super().__init__(parent, padding=10)
        self.appState: AppState = state
        self.controller: AppController = controller

        self.appState.subscribe(self._on_state_changed)
        self._build_ui()
        # Last TopicResult rendered; the panel only rebuilds when this changes
        # so parameter writes do not re-insert the per-document table (M3).
        self._last_result = None
        self._render()

    def _build_ui(self):
        self.lbl_title = ttk.Label(self, text="Summary & Info", font=("Helvetica", 12, "bold"))
        self.lbl_title.pack(anchor=W, pady=(0, 10))

        # Container for dynamic content
        self.content_frame = ttk.Frame(self)
        self.content_frame.pack(fill=BOTH, expand=YES)

        # Initial render to show placeholder
        self._render()

    def _on_state_changed(self, state: AppState):
        self._render()

    def _render(self):
        result = self.appState.current_result
        if result is self._last_result:
            # No new result; skip the full rebuild (M3). The content depends
            # only on the TopicResult, not on other state changes.
            return
        self._last_result = result

        # Clear current content
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        if not result:
            # Create a new placeholder since the old one was destroyed
            placeholder = ttk.Label(
                self.content_frame,
                text="[No model detected]\nPlease train new topic model",
                justify=CENTER
            )
            placeholder.pack(pady=20)
            return

        # 1. Basic Stats
        stats_frame = ttk.Frame(self.content_frame)
        stats_frame.pack(fill=X, pady=(0, 20))

        info_text = (
            f"Documents: {result.model_info.get('num_documents', 'Unknown')} | "
            f"Topics: {result.model_info.get('num_topics', 'Unknown')}"
        )
        ttk.Label(stats_frame, text=info_text, font=("Helvetica", 10, "bold")).pack(side=LEFT)

        # 2. Topics Table
        ttk.Label(self.content_frame, text="Top Topics", font=("Helvetica", 11, "bold")).pack(anchor=W)
        self._create_table(self.content_frame, "topics", result.topics)

        # 3. Doc-Topic Assignments Table
        ttk.Label(self.content_frame, text="Document Assignments", font=("Helvetica", 11, "bold")).pack(anchor=W, pady=(20, 0))
        self._create_table(self.content_frame, "doc_topics", result.doc_topics)

        # Force UI layout update
        self.update_idletasks()

    def _create_table(self, parent, type_key, data):
        """Helper to create a scrollable table for topic data."""
        container = ttk.Frame(parent)
        container.pack(fill=BOTH, expand=YES, pady=5)

        # Scrollbar and Treeview
        tree_frame = ttk.Frame(container)
        tree_frame.pack(fill=BOTH, expand=YES)

        columns = []
        if type_key == "topics":
            # Topics are List[Dict[term, weight]]
            columns = ("Topic ID", "Word 1", "Weight 1", "Word 2", "Weight 2", "Word 3", "Weight 3")
        else:
            # Doc topics are List[Dict[topic_id, prob]]
            # Expand to show top 3 topic assignments per document
            columns = ("Doc Index", "Topic 1", "Prob 1", "Topic 2", "Prob 2", "Topic 3", "Prob 3")

        tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            height=5,
            bootstyle="info"
        )

        vsb = ttk.Scrollbar(tree_frame, orient=VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)

        tree.pack(side=LEFT, fill=BOTH, expand=YES)
        vsb.pack(side=RIGHT, fill=Y)

        for col in columns:
            tree.heading(col, text=col)
            # Center IDs and Weights, left-align words
            alignment = CENTER if "ID" in col or "Weight" in col or "Prob" in col else W
            tree.column(col, width=100, anchor=alignment)

        # Populate data
        if type_key == "topics":
            for i, topic_dict in enumerate(data):
                # Get top 3 words sorted by weight
                sorted_words = sorted(topic_dict.items(), key=lambda x: x[1], reverse=True)[:3]

                # Create a list of 6 values (word, weight) x 3
                row_values = []
                for j in range(3):
                    if j < len(sorted_words):
                        word, weight = sorted_words[j]
                        row_values.extend([word, f"{weight:.2f}"])
                    else:
                        row_values.extend(["", ""])

                tree.insert("", END, values=(i, *row_values))
        else:
            # Cap the per-document table so a large corpus does not render
            # tens of thousands of Treeview rows (audit M3).
            max_rows = 200
            for i, doc_dict in enumerate(data[:max_rows]):
                if not doc_dict:
                    tree.insert("", END, values=(i, "N/A", "0.00", "N/A", "0.00", "N/A", "0.00"))
                    continue

                # Get top 3 topics sorted by probability
                sorted_topics = sorted(doc_dict.items(), key=lambda x: x[1], reverse=True)[:3]

                # Create a list of 6 values (topic_id, prob) x 3
                row_values = []
                for j in range(3):
                    if j < len(sorted_topics):
                        topic_id, prob = sorted_topics[j]
                        row_values.extend([f"Topic {topic_id}", f"{prob:.4f}"])
                    else:
                        row_values.extend(["N/A", "0.0000"])

                tree.insert("", END, values=(i, *row_values))

            if len(data) > max_rows:
                ttk.Label(
                    container,
                    text=f"Showing first {max_rows} of {len(data)} documents.",
                    bootstyle="secondary"
                ).pack(pady=2)
