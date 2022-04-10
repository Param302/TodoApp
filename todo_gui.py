from asyncio import create_task
import os
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from ttkbootstrap import style
from PIL import Image, ImageTk
from helper import TodayDateTime

WIDTH = 600
HEIGHT = 800
DARK = True
path = os.getcwd() + "/" + "Todo App/" if "Todo App" not in os.getcwd() else ""
path += "assets"
data = [eval(i[:-1]) for i in open(f"{path}/data.txt").readlines()]
WIDTH, HEIGHT, DARK, taskno = data


class TodoApp(tk.Tk):

    def __init__(self) -> None:
        super().__init__()
        self.todaydt = TodayDateTime()
        self._gui_configs()

    def _gui_configs(self) -> None:
        self.WIN_WIDTH = self.winfo_screenwidth()
        self.WIN_HEIGHT = self.winfo_screenheight()
        x = self.WIN_WIDTH//2 - WIDTH//2
        y = self.WIN_HEIGHT//2 - HEIGHT//2
        self.geometry(f"{WIDTH}x{HEIGHT}+{x}+{y}")
        self.title("Todo App")
        self.iconbitmap(f"{path}/icon.ico")
        self._font = "Segoe UI" if "Segoe UI" in tkFont.families() else "Arial"
        x = style.Style(theme="darkly")
        self.configure(background=x.colors.success)
        # style.Style().configure("TButton", font=(self._font, 20, "bold"))

    def _header(self) -> None:
        """Make Header having App name, 
        day-night btn and Date & time"""

        self._headerframe = ttk.Frame(
            self, style="success.TFrame", padding=(10, 0, 10, 5))

        self._appname = ttk.Label(self._headerframe, text="Daily Todo", style="success.Inverse.TLabel",
                                  font=(self._font, 24, "bold"), padding=(WIDTH//3, 0, WIDTH//3.7, 0))
        self._appname.grid(row=0, column=0, columnspan=3)

        self._img = ImageTk.PhotoImage(Image.open(
            f"{path}/{'sun.png' if DARK else 'moon.png'}").resize((25, 25)))
        self._modebtn = ttk.Button(self._headerframe, image=self._img,
                                   style="success.TButton", command=self._change_mode)
        self._modebtn.grid(row=0, column=3, ipadx=6, ipady=8)

        self._timelbl = ttk.Label(self._headerframe, font=(self._font, 12),
                                  text=self.todaydt.get_current_time().lower(), style="success.Inverse.TLabel")
        self._timelbl.grid(row=1, column=0, sticky="w")
        self._progressbar = ttk.Progressbar(self._headerframe, maximum=100, value=25,
                                            length=WIDTH//3, style="warning.Horizontal.TProgressbar")
        self._progressbar.grid(row=1, column=1, ipadx=70)
        self._headerframe.pack(side="top", fill="x")
        self._sep1 = ttk.Separator(
            self, orient="horizontal", style="TSeparator")
        self._sep1.pack(side="top", fill="x")

    def _todo_area(self):
        """Main area of window where All todo's are displayed"""
        self._todoframe = ttk.Frame(self, style="success.TFrame",
                                    padding=(WIDTH//8, 10))

        self._todoframe.pack(side="top", fill="both", expand=1)

    def _footer(self):
        """Footer to create new Todo"""
        self._footerframe = ttk.Frame(
            self, style="success.TFrame", padding=(0, 0, 0, HEIGHT//20))

        self._newtask = tk.StringVar(self, "Add new Task")
        self._addentry = ttk.Entry(self._footerframe, text=self._newtask,
                                   font=(self._font, 12), width=WIDTH//14,
                                   state="readonly")
        self._addentry.grid(row=0, column=0)
        self._addentry.bind("<Button-1>", lambda e: e.widget.configure(state="active")
                                or self._newtask.set("") or self._addbtn.configure(state="active"))
        self._addentry.bind(
            "<KeyRelease>", lambda e: e.widget.unbind(sequence="<Button-1>"))
        self._addentry.bind("<Return>", lambda e: self._add_task())

        self._addimg = ImageTk.PhotoImage(
            Image.open(f"{path}/add.png").resize((20, 20)))
        self._addbtn = ttk.Button(self._footerframe, image=self._addimg,
                                  state="disabled", style="success.TButton",
                                  command=self._add_task)
        self._addbtn.grid(row=0, column=1)

        self._footerframe.pack(side="bottom", fill="x", padx=WIDTH//8)

    def _add_task(self):
        """Callback to add a new Task"""
        global taskno
        task = self._newtask.get()
        if not task:
            return

        self._create_task(taskno=taskno, taskname=task)
        taskno += 1
        self._addentry.bind("<Button-1>", lambda e: e.widget.configure(state="active")
                            or self._newtask.set("") or self._addbtn.configure(state="active"))
        self._newtask.set("Add new task")
        self._addentry.configure(state="readonly")
        self._addbtn.configure(state="disabled")

    def _create_task(self, *, taskno: int, taskname: str):
        """Creates a Task"""
        _task = ttk.Frame(
            self._todoframe, style="info.TFrame", padding=(10, 0))
        _tasklbl = ttk.Label(_task, text=taskname, font=(self._font, 14),
                             style="warning.Inverse.TLabel")
        _tasklbl.grid(row=0, column=1, padx=10, pady=5)
        _task.grid(row=taskno-1, column=0, sticky="w")

    def _change_mode(self):
        """Change night mode to day mode and vice-versa."""
        global DARK
        self._img = ImageTk.PhotoImage(Image.open(
            f"{path}/{'moon.png' if DARK else 'sun.png'}").resize((25, 25)))
        self._modebtn.configure(image=self._img)
        DARK = not DARK
        print("called")

    def run(self):
        self._header()
        self._todo_area()
        self._footer()
        self.mainloop()


if __name__ == "__main__":
    todoapp = TodoApp()
    todoapp.run()
