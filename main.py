from Tui import TodoApp
from dbmanager import tododatabase
if __name__ == "__main__":
    class Todolistapp(TodoApp):
        def __init__(self, driver_class=None, css_path=None, watch_css=False, ansi_color=False):
            self.DBcontrol = tododatabase()
            
            super().__init__(driver_class, css_path, watch_css, ansi_color)
    Todolistapp().run()