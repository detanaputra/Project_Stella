import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import Scrollbar, messagebox, simpledialog
from app.models.app_state import AppState
from app.controllers.app_controller import AppController
from app.models.topic_result import TopicResult

class SummaryPanel(ttk.Frame):
    """Panel for displaying summary information and key metrics."""

    # Sentinel distinct from None: the first _render() (current_result is None
    # on a fresh start) must not be mistaken for an already-rendered state, or
    # the "[No model detected]" placeholder would never be drawn (M3 fix).
    _NEVER_RENDERED = object()

    def __init__(self, parent, state: AppState, controller: AppController):
        super().__init__(parent, padding=10)
        self.appState: AppState = state
        self.controller: AppController = controller
        # Must be set before _build_ui(): it calls _render(), which reads it.
        self._last_result = self._NEVER_RENDERED
        # Checked topic ids for refinement (v0.4.0, WP1).
        self._selected_topics = set()
        self._btn_merge = None
        self._btn_delete = None
        self._btn_label = None

        self.appState.subscribe(self._on_state_changed)
        self._build_ui()
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
        # Selection resets when the result changes (topic ids change after a
        # refinement, so a stale selection would be meaningless).
        self._selected_topics = set()

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

        # 2. Refinement toolbar (after basic stats, before the topics table)
        self._build_toolbar(self.content_frame)

        # 3. Topics Table
        ttk.Label(self.content_frame, text="Top Topics", font=("Helvetica", 11, "bold")).pack(anchor=W)
        self._create_topics_table(self.content_frame, result)

        # 4. Doc-Topic Assignments Table
        ttk.Label(self.content_frame, text="Document Assignments", font=("Helvetica", 11, "bold")).pack(anchor=W, pady=(20, 0))
        self._create_doc_topics_table(self.content_frame, result.doc_topics)

        # Force UI layout update
        self.update_idletasks()

    # --- Refinement toolbar (v0.4.0, WP1) -----------------------------------

    def _build_toolbar(self, parent):
        """Refinement toolbar (icon + text): merge, delete, label."""
        toolbar = ttk.Frame(parent)
        toolbar.pack(fill=X, pady=(0, 10))
        self._btn_merge = ttk.Button(
            toolbar, icon="sign-merge-left", icon_only=False, bootstyle="primary",
            command=self._on_merge, text="Merge")
        self._btn_merge.pack(side=LEFT, padx=(0, 4))
        self._btn_delete = ttk.Button(
            toolbar, icon="trash", icon_only=False, bootstyle="danger",
            command=self._on_delete, text="Delete")
        self._btn_delete.pack(side=LEFT, padx=(0, 4))
        self._btn_label = ttk.Button(
            toolbar, icon="tag", icon_only=False, bootstyle="primary",
            command=self._on_label, text="Label")
        self._btn_label.pack(side=LEFT)
        self._update_toolbar_state()

    def _update_toolbar_state(self):
        """Enable buttons by selection count: delete 1+, merge 2+, label 1."""
        n = len(self._selected_topics)
        if self._btn_merge is not None:
            self._btn_merge.config(state="normal" if n >= 2 else "disabled")
        if self._btn_delete is not None:
            self._btn_delete.config(state="normal" if n >= 1 else "disabled")
        if self._btn_label is not None:
            self._btn_label.config(state="normal" if n == 1 else "disabled")

    def _on_merge(self):
        if len(self._selected_topics) < 2:
            return
        topic_ids = sorted(self._selected_topics)
        if not messagebox.askyesno(
            "Merge Topics",
            f"Merge topics {topic_ids} into one? This cannot be undone.",
            parent=self,
        ):
            return
        self._show_loading()
        self.controller.merge_topics(topic_ids)

    def _on_delete(self):
        if not self._selected_topics:
            return
        topic_ids = sorted(self._selected_topics)
        if not messagebox.askyesno(
            "Delete Topics",
            f"Delete topic(s) {topic_ids}? Their documents will become outliers. "
            "This cannot be undone.",
            parent=self,
        ):
            return
        self._show_loading()
        self.controller.delete_topics(topic_ids)

    def _on_label(self):
        if len(self._selected_topics) != 1:
            return
        topic_id = next(iter(self._selected_topics))
        label = simpledialog.askstring(
            "Label Topic",
            f"Enter a name or interpretation for topic {topic_id}:",
            parent=self,
        )
        if label is not None and label.strip():
            self.controller.label_topic(topic_id, label.strip())

    def _show_loading(self):
        root = self.winfo_toplevel()
        if hasattr(root, "show_loading_panel"):
            root.show_loading_panel()

    # --- Tables -------------------------------------------------------------

    def _create_topics_table(self, parent, result: TopicResult):
        """Topics table with a leading checkbox column (v0.4.0, WP1).

        Clicking anywhere on a row toggles its checkbox; the state is mirrored
        into the Treeview's native selection so the row also highlights.
        """
        container = ttk.Frame(parent)
        container.pack(fill=BOTH, expand=YES, pady=5)

        tree_frame = ttk.Frame(container)
        tree_frame.pack(fill=BOTH, expand=YES)

        columns = ("✓", "Topic ID", "Word 1", "Weight 1", "Word 2", "Weight 2", "Word 3", "Weight 3")
        tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            height=5,
            bootstyle="info",
            selectmode="none",  # selection is driven by the checkbox column
        )

        vsb = ttk.Scrollbar(tree_frame, orient=VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)

        tree.pack(side=LEFT, fill=BOTH, expand=YES)
        vsb.pack(side=RIGHT, fill=Y)

        for col in columns:
            tree.heading(col, text=col)
            # Center IDs and Weights, left-align words
            alignment = CENTER if "ID" in col or "Weight" in col or col == "✓" else W
            tree.column(col, width=100, anchor=alignment)
        tree.column("✓", width=30, stretch=False)

        labels = result.topic_labels or {}
        for i, topic_dict in enumerate(result.topics):
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

            label = labels.get(i)
            topic_display = f"{i} — {label}" if label else str(i)
            # iid = topic id, so identify_row() gives us the topic id directly.
            tree.insert("", END, iid=str(i), values=("☐", topic_display, *row_values))

        tree.bind("<Button-1>", self._on_topic_click)

    def _on_topic_click(self, event):
        """Toggle a topic's checkbox when any part of its row is clicked."""
        tree = event.widget
        row_id = tree.identify_row(event.y)
        if not row_id:
            return
        topic_id = int(row_id)  # iid is the topic id
        if topic_id in self._selected_topics:
            self._selected_topics.discard(topic_id)
            tree.set(row_id, "✓", "☐")
            tree.selection_remove(row_id)
        else:
            self._selected_topics.add(topic_id)
            tree.set(row_id, "✓", "☑")
            tree.selection_add(row_id)
        self._update_toolbar_state()

    def _create_doc_topics_table(self, parent, data):
        """Doc-topic assignments table."""
        container = ttk.Frame(parent)
        container.pack(fill=BOTH, expand=YES, pady=5)

        tree_frame = ttk.Frame(container)
        tree_frame.pack(fill=BOTH, expand=YES)

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
