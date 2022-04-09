import tkinter as tk
from tkinter import ttk
from ttkbootstrap import style

WIDTH = 600
HEIGHT = 800


class TodoApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.WIN_WIDTH = self.winfo_screenwidth()
        self.WIN_HEIGHT = self.winfo_screenheight()
        self._gui_configs()

    def _gui_configs(self):
        x = self.WIN_WIDTH//2 - WIDTH//2
        y = self.WIN_HEIGHT//2 - HEIGHT//2
        self.geometry(f"{WIDTH}x{HEIGHT}+{x}+{y}")
        self.title("Todo App")
        self.iconbitmap("./assets/icon.ico")

    def _header(self):
        """Make Header having App name, 
        day-night btn and Date & time"""

    def _todo_area(self):
        """Main area of window where All todo's are displayed"""

    def _footer(self):
        """Footer to create new Todo"""

    def _create_task(self):
        """Creates a task"""

    def run(self):
        self.mainloop()


if __name__ == "__main__":
    todoapp = TodoApp()
    todoapp.run()
