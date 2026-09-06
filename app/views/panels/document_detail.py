"""Detail view for a single document (v0.4.0, WP4).

Opened from the Document Assignments table's "Detail" button: shows the doc
index, all topic→probability assignments, and the full document text in a
scrollable read-only Text (paragraphs supported).
"""

import tkinter as tk
from tkinter import Toplevel, scrolledtext

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from app.models.topic_result import TopicResult
from app.views.window_utils import center_on_parent


class DocumentDetailWindow(Toplevel):
    """A centered Top-Level window showing one document's full detail."""

    def __init__(self, parent, result: TopicResult, doc_index: int):
        super().__init__(parent)
        self.title(f"Document {doc_index}")
        self.withdraw()  # keep hidden until positioned (v0.4.0, WP3)
        self.transient(parent)

        doc_topics = result.doc_topics[doc_index] if doc_index < len(result.doc_topics) else {}
        original_texts = result.metadata.get('original_texts') or []
        text = original_texts[doc_index] if doc_index < len(original_texts) else ""

        # Header
        ttk.Label(self, text=f"Document {doc_index}", font=("Helvetica", 14, "bold")).pack(
            anchor=W, padx=20, pady=(20, 10))

        # All topic assignments
        topics_frame = ttk.LabelFrame(self, text="Topic Assignments", padding=8)
        topics_frame.pack(fill=X, padx=20, pady=(0, 10))
        if doc_topics:
            tree = ttk.Treeview(
                topics_frame,
                columns=("Topic", "Probability"),
                show="headings",
                height=min(len(doc_topics), 8),
                bootstyle="info",
            )
            tree.heading("Topic", text="Topic")
            tree.heading("Probability", text="Probability")
            tree.column("Topic", width=120, anchor=CENTER)
            tree.column("Probability", width=120, anchor=CENTER)
            for topic_id, prob in sorted(doc_topics.items(), key=lambda x: x[1], reverse=True):
                tree.insert("", END, values=(f"Topic {topic_id}", f"{prob:.4f}"))
            tree.pack(fill=X)
        else:
            ttk.Label(topics_frame, text="No topic assignments.", bootstyle="secondary").pack(anchor=W)

        # Full document (scrollable, read-only)
        doc_frame = ttk.LabelFrame(self, text="Document", padding=8)
        doc_frame.pack(fill=BOTH, expand=YES, padx=20, pady=(0, 20))
        text_widget = scrolledtext.ScrolledText(doc_frame, wrap=tk.WORD, height=12)
        text_widget.pack(fill=BOTH, expand=YES)
        text_widget.insert("1.0", text)
        text_widget.config(state="disabled")  # read-only

        ttk.Button(self, text="Close", command=self.destroy, bootstyle="secondary").pack(pady=(0, 0))

        center_on_parent(self, parent, 700, 600)
        self.deiconify()  # show centered, no position flash
        self.grab_set()
