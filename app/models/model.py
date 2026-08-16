class Model:
    """
    The Model handles the data and business logic of the application.
    It should be independent of the UI.
    """
    def __init__(self):
        self._data = "Hello, Stella!"

    def get_data(self):
        return self._data

    def set_data(self, new_data):
        self._data = new_data
        # In a real app, you might notify observers here
