import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from app.models.app_state import AppState
from app.controllers.app_controller import AppController
from app.controllers.analysis_controller import AnalysisController
from app.views.menu_manager import MenuManager
from app.views.panels.summary_panel import SummaryPanel
from app.views.panels.algorithm_settings_panel import AlgorithmSettingsPanel
from app.views.panels.loading_panel import LoadingPanel
from app.views.panels.export_panel import ExportPanel
from app.views.panels.metric_panel import MetricPanel
from app.views.panels.static_viz_panel import StaticVizPanel
from app.views.window_utils import center_on_parent

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

        # --- Left Column: Algorithm Parameters (persistent, v0.3.0 WP2) ---
        self.algo_settings_panel = AlgorithmSettingsPanel(
            self.root_pane, self.appState, self.app_controller, self.analysis_controller
        )
        self.root_pane.add(self.algo_settings_panel, weight=1)

        # --- Right Column: Main Content (Notebook) ---
        self.main_notebook = ttk.Notebook(self.root_pane)
        self.root_pane.add(self.main_notebook, weight=6)

        # Analysis Tab: summary only (params moved to the left column, v0.3.0 WP2)
        self.tab_analysis = ttk.Frame(self.main_notebook)
        self.main_notebook.add(self.tab_analysis, text=" Analysis ")
        self.summary_panel = SummaryPanel(self.tab_analysis, self.appState, self.app_controller)
        self.summary_panel.pack(fill=BOTH, expand=YES)

        # configure the thickness of Sash in Panedwindow so it is easier to grab
        self.style.configure("Sash", sashthickness=8)

    def _apply_theme(self, theme_name: str) -> None:
        """Apply the selected ttkbootstrap theme to the whole application."""
        self.style.theme_use(theme_name)

    def open_export_dialog(self):
        """Open the Export panel in a modal dialog (v0.3.0, WP2)."""
        dialog = ttk.Toplevel(self)
        dialog.title("Export Results")
        dialog.withdraw()  # keep hidden until positioned (v0.4.0, WP3)
        dialog.transient(self)
        panel = ExportPanel(dialog, self.appState, self.app_controller)
        panel.pack(fill=BOTH, expand=YES)
        ttk.Button(dialog, text="Close", command=dialog.destroy).pack(pady=8)
        center_on_parent(dialog, self, 420, 440)
        dialog.deiconify()  # show centered, no position flash
        dialog.grab_set()

    def open_settings_dialog(self):
        """Open the App Settings (theme switcher) in a modal dialog (v0.3.0, WP2)."""
        dialog = ttk.Toplevel(self)
        dialog.title("App Settings")
        dialog.withdraw()  # keep hidden until positioned (v0.4.0, WP3)
        dialog.transient(self)
        frame = ttk.Frame(dialog, padding=20)
        frame.pack(fill=BOTH, expand=YES)
        ttk.Label(frame, text="App Settings", font=("Helvetica", 14, "bold")).pack(anchor=W, pady=(0, 12))
        theme_frame = ttk.Frame(frame)
        theme_frame.pack(fill=X, pady=6)
        ttk.Label(theme_frame, text="Theme:", width=16).pack(side=LEFT)
        theme_var = ttk.StringVar(value=self.style.theme.name)
        theme_combo = ttk.Combobox(
            theme_frame,
            textvariable=theme_var,
            values=sorted(self.style.theme_names()),
            state="readonly"
        )
        theme_combo.pack(side=LEFT, fill=X, expand=YES)
        theme_combo.bind("<<ComboboxSelected>>", lambda e: self._apply_theme(theme_var.get()))
        ttk.Button(dialog, text="Close", command=dialog.destroy).pack(pady=8)
        center_on_parent(dialog, self, 360, 180)
        dialog.deiconify()  # show centered, no position flash
        dialog.grab_set()

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
            # Append ("end") — integer indices fail when the notebook has few
            # tabs (v0.3.0 WP2 removed the Export/Settings tabs).
            self.main_notebook.insert("end", self._metrics_tab, text=" Metrics ")
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
            # Append in order after Metrics (Metrics is added first by
            # _sync_metrics_tab); "end" avoids integer-index bounds errors.
            for viz_name, title in _VIZ_TABS:
                tab = ttk.Frame(self.main_notebook)
                panel = StaticVizPanel(tab, self.appState, self.app_controller, viz_name, title)
                panel.pack(fill=BOTH, expand=YES)
                self.main_notebook.insert("end", tab, text=f" {title} ")
                self._viz_tabs.append(tab)
                self._viz_panels.append(panel)
        elif not has_result and self._viz_tabs is not None:
            for tab in self._viz_tabs:
                self.main_notebook.forget(tab)
            self._viz_tabs = None
            self._viz_panels = None

    def _poll_state_events(self):
        """Check the AppState event queue and update views."""
        try:
            self.appState.process_events()
        finally:
            # Always re-schedule, even if process_events raises, so a single
            # bad callback cannot freeze all future UI updates (audit H5).
            self.after(100, self._poll_state_events)
