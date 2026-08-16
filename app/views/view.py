import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class View(ttk.Window):
    """
    The View handles the presentation layer using ttkbootstrap.
    It does not contain business logic.
    """
    def __init__(self):
        super().__init__(themename="superhero")
        self.title("Project Stella - MVC Scaffold")
        self.geometry("1280x720")

        self.container = ttk.Frame(self, padding=20)
        self.container.pack(fill=BOTH, expand=YES)

        self.label = ttk.Label(
            self.container,
            text="Welcome",
            font=("Helvetica", 14),
            bootstyle="light"
        )
        self.label.pack(pady=10)

        self.entry = ttk.Entry(self.container)
        self.entry.pack(pady=10)

        self.button = ttk.Button(
            self.container,
            text="Update Text",
            bootstyle="primary"
        )
        self.button.pack(pady=10)

    def update_label(self, text):
        self.label.config(text=text)

    def get_entry_text(self):
        return self.entry.get()

    def set_controller(self, controller):
        """Binds the button click to the controller's method."""
        self.button.config(command=controller.handle_button_click)
