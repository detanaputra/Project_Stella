from app.models.app_state import AppState
from app.views.main_window import MainWindow
import multiprocessing

def main():
    # 1. Initialize the single source of truth
    state = AppState()

    # 2. Launch the GUI
    app = MainWindow(state)

    # 3. Start the application
    app.mainloop()

if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
