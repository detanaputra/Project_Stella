import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from app.models.app_state import AppState
from app.controllers.app_controller import AppController
from app.controllers.analysis_controller import AnalysisController
from app.views.menu_manager import MenuManager
from app.views.panels.toolbox_panel import ToolboxPanel
from app.views.panels.summary_panel import SummaryPanel
from app.views.panels.algorithm_settings_panel import AlgorithmSettingsPanel
from app.views.panels.loading_panel import LoadingPanel
from app.views.panels.export_panel import ExportPanel
from app.views.panels.metric_panel import MetricPanel
from app.views.panels.static_viz_panel import StaticVizPanel

# The 5 BERTopic visualisations exposed as static tabs (v0.3.0, WP1).
_VIZ_TABS = [
    ("topics", "Topics"),
    ("heatmap", "Heatmap"),
    ("barchart", "Barchart"),
    ("hierarchy", "Hierarchy"),
    ("term_rank", "Term Rank"),
]

class MainWindow(ttk.Window):
    """
    Main Application Window.
    Coordinates the layout and poles the AppState event queue to trigger UI updates.
    """
    def __init__(self, state: AppState):
        super().__init__(themename="flatly")
        self.title("Project Stella - Semantic Topic ExpLoration and LeArning")
        self.geometry("1280x720")

        self.appState: AppState = state
        self.app_controller = AppController(state)
        self.analysis_controller = AnalysisController(state)

        # Global Menu Management
        self.menu_manager = MenuManager(self, self.app_controller)
        self.menu_manager.build_menu()

        self._build_ui()
        self.main_notebook.bind("<<NotebookTabChanged>>", self._on_tab_changed)

        # Metrics tab: created dynamically once a result exists (v0.2.0).
        self._metrics_tab = None
        self._metrics_panel = None
        # Visualisation tabs: created dynamically once a result exists (v0.3.0, WP1).
        self._viz_tabs = None
        self._viz_panels = None
        self.appState.subscribe(self._on_state_changed)

        # Start polling the event queue
        self._poll_state_events()

    def show_loading_panel(self):
        """Launch the loading overlay.

        Reuses the existing instance when one is already open so repeated
        calls (e.g. a double-click on Train) cannot stack modal dialogs
        (audit L4).
        """
        existing = getattr(self, '_loading_panel', None)
        if existing is not None:
            try:
                if existing.winfo_exists():
                    existing.lift()
                    existing.focus_force()
                    return
            except tk.TclError:
                pass  # panel was destroyed (analysis finished); create a fresh one
        self._loading_panel = LoadingPanel(self, self.appState, self.app_controller)

    def _build_ui(self):
        # Root Layout: PanedWindow (Horizontal)
        self.root_pane = ttk.Panedwindow(self, orient=HORIZONTAL)
        self.root_pane.pack(fill=BOTH, expand=YES)

        # --- Left Column: Toolbox ---
        self.toolbox_panel = ToolboxPanel(self.root_pane, self.appState, self.app_controller)
        self.root_pane.add(self.toolbox_panel, weight=1)

        # --- Right Column: Main Content (Notebook) ---
        self.main_notebook = ttk.Notebook(self.root_pane)
        self.root_pane.add(self.main_notebook, weight=6)

        # Analysis Tab
        self.tab_analysis = ttk.Frame(self.main_notebook)
        self.main_notebook.add(self.tab_analysis, text=" Analysis ")

        # Inside Analysis Tab: PanedWindow (Horizontal)
        self.content_pane = ttk.Panedwindow(self.tab_analysis, orient=HORIZONTAL)
        self.content_pane.pack(fill=BOTH, expand=YES)

        # Left: Summary / Informative Content
        self.summary_panel = SummaryPanel(self.content_pane, self.appState, self.app_controller)
        self.content_pane.add(self.summary_panel, weight=5)

        # Right: Algorithm Parameters
        self.algo_settings_panel = AlgorithmSettingsPanel(self.content_pane, self.appState, self.app_controller, self.analysis_controller)
        self.content_pane.add(self.algo_settings_panel, weight=1)

        # Export tab: real CSV/JSON/report export and browser visualizations
        # (audit M4 — previously a mock-up label).
        self.tab_export = ttk.Frame(self.main_notebook)
        self.main_notebook.add(self.tab_export, text=" Export ")
        self.export_panel = ExportPanel(self.tab_export, self.appState, self.app_controller)
        self.export_panel.pack(fill=BOTH, expand=YES)

        # App Settings tab: real theme switcher (audit L1 — was a mockup label).
        self.tab_settings = ttk.Frame(self.main_notebook)
        self.main_notebook.add(self.tab_settings, text=" App Settings ")

        settings_frame = ttk.Frame(self.tab_settings, padding=20)
        settings_frame.pack(fill=BOTH, expand=YES)

        ttk.Label(settings_frame, text="App Settings", font=("Helvetica", 14, "bold")).pack(anchor=W, pady=(0, 12))

        theme_frame = ttk.Frame(settings_frame)
        theme_frame.pack(fill=X, pady=6)
        ttk.Label(theme_frame, text="Theme:", width=16).pack(side=LEFT)
        self.theme_var = ttk.StringVar(value=self.style.theme.name)
        theme_combo = ttk.Combobox(
            theme_frame,
            textvariable=self.theme_var,
            values=sorted(self.style.theme_names()),
            state="readonly"
        )
        theme_combo.pack(side=LEFT, fill=X, expand=YES)
        theme_combo.bind("<<ComboboxSelected>>", self._on_theme_changed)

        # configure the thichness of Sash in Pannedwindow so it is easier to grab
        self.style.configure("Sash", sashthickness=8)

    def _on_theme_changed(self, event=None) -> None:
        """Apply the selected ttkbootstrap theme to the whole application."""
        self.style.theme_use(self.theme_var.get())

    def _on_state_changed(self, state: AppState):
        self._sync_metrics_tab()
        self._sync_viz_tabs()

    def _sync_metrics_tab(self):
        """Add the Metrics tab after Analysis once a result exists; remove it
        when the result is cleared (v0.2.0)."""
        has_result = self.appState.current_result is not None
        if has_result and self._metrics_tab is None:
            self._metrics_tab = ttk.Frame(self.main_notebook)
            self._metrics_panel = MetricPanel(self._metrics_tab, self.appState, self.app_controller)
            self._metrics_panel.pack(fill=BOTH, expand=YES)
            self.main_notebook.insert(1, self._metrics_tab, text=" Metrics ")
        elif not has_result and self._metrics_tab is not None:
            self.main_notebook.forget(self._metrics_tab)
            self._metrics_tab = None
            self._metrics_panel = None

    def _sync_viz_tabs(self):
        """Add the 5 visualisation tabs after Metrics once a result exists;
        remove them when the result is cleared (v0.3.0, WP1)."""
        has_result = self.appState.current_result is not None
        if has_result and self._viz_tabs is None:
            self._viz_tabs = []
            self._viz_panels = []
            insert_pos = 1  # after Analysis
            if self._metrics_tab is not None:
                insert_pos = self.main_notebook.index(self._metrics_tab) + 1
            for viz_name, title in _VIZ_TABS:
                tab = ttk.Frame(self.main_notebook)
                panel = StaticVizPanel(tab, self.appState, self.app_controller, viz_name, title)
                panel.pack(fill=BOTH, expand=YES)
                self.main_notebook.insert(insert_pos, tab, text=f" {title} ")
                self._viz_tabs.append(tab)
                self._viz_panels.append(panel)
                insert_pos += 1
        elif not has_result and self._viz_tabs is not None:
            for tab in self._viz_tabs:
                self.main_notebook.forget(tab)
            self._viz_tabs = None
            self._viz_panels = None

    def _on_tab_changed(self, event=None):
        """Lazy-render the selected visualisation tab (v0.3.0, WP1)."""
        if self._viz_panels is None:
            return
        selected = self.main_notebook.select()
        for tab, panel in zip(self._viz_tabs, self._viz_panels):
            if str(tab) == str(selected):
                panel.ensure_rendered()
                break

    def _poll_state_events(self):
        """Check the AppState event queue and update views."""
        try:
            self.appState.process_events()
        finally:
            # Always re-schedule, even if process_events raises, so a single
            # bad callback cannot freeze all future UI updates (audit H5).
            self.after(100, self._poll_state_events)
