class Controller:
    """
    The Controller acts as the glue between the Model and the View.
    It handles user input and updates the model and view accordingly.
    """
    def __init__(self, model, view):
        self.model = model
        self.view = view

        # Initialize the view with data from the model
        self.update_view()

        # Connect the view to this controller
        self.view.set_controller(self)

    def handle_button_click(self):
        # Get input from view
        new_text = self.view.get_entry_text()
        if new_text:
            # Update model
            self.model.set_data(new_text)
            # Update view
            self.update_view()

    def update_view(self):
        data = self.model.get_data()
        self.view.update_label(data)
