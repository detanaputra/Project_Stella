import tkinter as tk
from app.views.menus.base_menu import BaseMenu

class WindowMenu(BaseMenu):
    def build(self, menubar: tk.Menu) -> tk.Menu:
            # Create the View menu
            menu = tk.Menu(menubar, tearoff=False)
    
            # Placeholder commands
            menu.add_command(label="Zoom In", command=self._on_zoom_in)
            menu.add_command(label="Zoom Out", command=self._on_zoom_out)
            menu.add_separator()
            
    
            return menu


    def _on_zoom_in(self) -> None:
            print("Menu Action: Zoom In")
    

    def _on_zoom_out(self) -> None:
        print("Menu Action: Zoom Out")