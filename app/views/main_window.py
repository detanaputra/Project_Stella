import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from app.models.app_state import AppState
from app.controllers.app_controller import AppController
from app.controllers.analysis_controller import AnalysisController
from app.views.menu_manager import MenuManager
from app.views.panels.toolbox_panel import ToolboxPanel
from app.views.panels.summary_panel import SummaryPanel
from app.views.panels.algorithm_settings_panel import AlgorithmSettingsPanel
from app.views.panels.input_panel import InputPanel
from app.views.panels.settings_panel import SettingsPanel
from app.views.panels.processing_panel import ProcessingPanel
from app.views.panels.results_panel import ResultsPanel
from app.views.panels.loading_panel import LoadingPanel

class MainWindow(ttk.Window):
    """
    Main Application Window.
    Coordinates the layout and poles the AppState event queue to trigger UI updates.
    """
    def __init__(self, state: AppState):
        super().__init__(themename="flatly")
        self.title("Project Stella - Semantic Topic ExpLoration LeArning")
        self.geometry("1280x720")

        self.appState: AppState = state
        self.app_controller = AppController(state)
        self.analysis_controller = AnalysisController(state)

        # Global Menu Management
        self.menu_manager = MenuManager(self, self.app_controller)
        self.menu_manager.build_menu()

        self._build_ui()

        # Start polling the event queue
        self._poll_state_events()

    def show_loading_panel(self):
        """Launch the loading overlay."""
        LoadingPanel(self, self.appState, self.app_controller)

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

        # Add other tabs as placeholders for now
        self.tab_export = ttk.Frame(self.main_notebook)
        self.main_notebook.add(self.tab_export, text=" Export ")
        ttk.Label(self.tab_export, text="Export Options Mock-up").pack(pady=20)

        self.tab_settings = ttk.Frame(self.main_notebook)
        self.main_notebook.add(self.tab_settings, text=" App Settings ")
        ttk.Label(self.tab_settings, text="Global App Settings Mock-up").pack(pady=20)

        # configure the thichness of Sash in Pannedwindow so it is easier to grab
        self.style.configure("Sash", sashthickness=8)

    def _poll_state_events(self):
        """Check the AppState event queue and update views."""
        self.appState.process_events()
        # Poll every 100ms
        self.after(100, self._poll_state_events)
