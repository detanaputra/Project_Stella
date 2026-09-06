import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import Scrollbar, messagebox, simpledialog
from app.models.app_state import AppState
from app.controllers.app_controller import AppController
from app.models.topic_result import TopicResult
from app.views.panels.document_detail import DocumentDetailWindow

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
        # Document exploration state (v0.4.0, WP4).
        self._search_query = ""
        self._search_var = None
        self._search_entry = None
        self._btn_search = None
        self._btn_clear = None
        self._btn_detail = None
        self._doc_table_frame = None
        self._doc_tree = None
        self._doc_filter_label = None

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
        # Search resets when the result changes.
        self._search_query = ""

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

        # 4. Document Assignments (search + detail + table)
        self._create_doc_topics_section(self.content_frame, result)

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
        # Re-filter the Document Assignments table by the selected topics.
        self._rebuild_doc_table()

    def _create_doc_topics_section(self, parent, result: TopicResult):
        """Document Assignments section: search box + Detail button + table (v0.4.0, WP4)."""
        section = ttk.Frame(parent)
        section.pack(fill=BOTH, expand=YES, pady=(20, 0))

        # Header row: title + Detail button
        header = ttk.Frame(section)
        header.pack(fill=X)
        ttk.Label(header, text="Document Assignments", font=("Helvetica", 11, "bold")).pack(side=LEFT)
        self._btn_detail = ttk.Button(header, icon="info-circle-fill", text="Detail", bootstyle="info", command=self._on_detail)
        self._btn_detail.pack(side=RIGHT)
        self._btn_detail.config(state="disabled")

        # Search row: entry + Search + Clear
        search_row = ttk.Frame(section)
        search_row.pack(fill=X, pady=(4, 0))
        self._search_var = ttk.StringVar()
        self._search_entry = ttk.Entry(search_row, textvariable=self._search_var, width=40)
        self._search_entry.pack(side=LEFT, padx=(0, 4))
        self._search_entry.bind("<Return>", lambda e: self._on_search())
        self._btn_search = ttk.Button(search_row, icon="search", text="Search", bootstyle="primary", command=self._on_search)
        self._btn_search.pack(side=LEFT, padx=(0, 4))
        self._btn_clear = ttk.Button(search_row, icon="x-circle-fill", text="Clear", bootstyle="secondary", command=self._on_clear_search)
        self._btn_clear.pack(side=LEFT)

        # Table frame (rebuilt on search/clear/topic selection)
        self._doc_table_frame = ttk.Frame(section)
        self._doc_table_frame.pack(fill=BOTH, expand=YES)
        self._build_doc_table(self._doc_table_frame, result)

        # Filter status label
        self._doc_filter_label = ttk.Label(section, text="", bootstyle="secondary")
        self._doc_filter_label.pack(anchor=W, pady=(2, 0))

    def _build_doc_table(self, parent, result: TopicResult):
        """Build the Document Assignments table with the current search filter.

        Columns: Doc Index · Document · Topic 1 · Prob 1. The Document cell shows
        the first 50 chars, or a window around the query match when searching.
        """
        for widget in parent.winfo_children():
            widget.destroy()

        container = ttk.Frame(parent)
        container.pack(fill=BOTH, expand=YES, pady=5)

        tree_frame = ttk.Frame(container)
        tree_frame.pack(fill=BOTH, expand=YES)

        columns = ("Doc Index", "Document", "Topic 1", "Prob 1")
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
            alignment = CENTER if "Index" in col or "Prob" in col else W
            tree.column(col, width=100, anchor=alignment)
        tree.column("Document", width=300)

        doc_topics = result.doc_topics
        original_texts = result.metadata.get('original_texts') or []
        query = self._search_query or ""
        query_lower = query.lower()

        # Matching doc indices (full-text, case-insensitive)
        if query_lower:
            matching = [
                i for i, d in enumerate(doc_topics)
                if i < len(original_texts) and query_lower in original_texts[i].lower()
            ]
        else:
            matching = list(range(len(doc_topics)))

        # Topic filter: when topics are selected in the topics table, show only
        # docs whose Topic 1 (argmax) is one of the selected topics.
        if self._selected_topics:
            matching = [
                i for i in matching
                if doc_topics[i]
                and max(doc_topics[i], key=doc_topics[i].get) in self._selected_topics
            ]

        # Cap the per-document table so a large corpus does not render
        # tens of thousands of Treeview rows (audit M3).
        max_rows = 200
        for i in matching[:max_rows]:
            doc_dict = doc_topics[i]
            text = original_texts[i] if i < len(original_texts) else ""
            snippet = self._doc_snippet(text, query_lower)
            if doc_dict:
                topic_id = max(doc_dict, key=doc_dict.get)
                prob = doc_dict[topic_id]
                tree.insert("", END, iid=str(i), values=(i, snippet, f"Topic {topic_id}", f"{prob:.4f}"))
            else:
                tree.insert("", END, iid=str(i), values=(i, snippet, "N/A", "0.0000"))

        if len(matching) > max_rows:
            ttk.Label(
                container,
                text=f"Showing first {max_rows} of {len(matching)} documents.",
                bootstyle="secondary"
            ).pack(pady=2)

        # Filter status
        if self._doc_filter_label is not None:
            parts = []
            if self._selected_topics:
                parts.append(f"{len(self._selected_topics)} selected topic(s)")
            if query_lower:
                parts.append(f"matching '{self._search_query}'")
            self._doc_filter_label.config(
                text=("Filtered by " + " and ".join(parts) + ".") if parts else "")

        self._doc_tree = tree
        tree.bind("<<TreeviewSelect>>", self._on_doc_select)
        self._update_detail_state()

    def _doc_snippet(self, text: str, query_lower: str) -> str:
        """First 50 chars, or a window around the query match when searching."""
        if not text:
            return ""
        if query_lower:
            idx = text.lower().find(query_lower)
            if idx != -1:
                start = max(0, idx - 20)
                end = min(len(text), idx + len(query_lower) + 20)
                snippet = text[start:end]
                if start > 0:
                    snippet = "…" + snippet
                if end < len(text):
                    snippet = snippet + "…"
                return snippet
        return text[:50]

    def _rebuild_doc_table(self):
        """Rebuild the Document Assignments table with the current filters
        (search query + selected topics)."""
        if self._doc_table_frame is not None and self.appState.current_result is not None:
            self._build_doc_table(self._doc_table_frame, self.appState.current_result)

    def _on_search(self):
        self._search_query = self._search_var.get().strip()
        self._rebuild_doc_table()

    def _on_clear_search(self):
        self._search_query = ""
        self._search_var.set("")
        self._rebuild_doc_table()

    def _on_doc_select(self, event):
        self._update_detail_state()

    def _update_detail_state(self):
        if self._btn_detail is not None:
            n = len(self._doc_tree.selection()) if self._doc_tree is not None else 0
            self._btn_detail.config(state="normal" if n == 1 else "disabled")

    def _on_detail(self):
        if self._doc_tree is None:
            return
        selection = self._doc_tree.selection()
        if len(selection) != 1:
            return
        result = self.appState.current_result
        if result is None:
            return
        root = self.winfo_toplevel()
        DocumentDetailWindow(root, result, int(selection[0]))
