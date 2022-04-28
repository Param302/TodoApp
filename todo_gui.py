import os
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from ttkbootstrap import style
from PIL import Image, ImageTk
from helper import TodayDateTime

WIDTH = 600
HEIGHT = 850
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
        y = 100
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

        self._headerframe = ttk.Frame(self, style="success.TFrame")

        self._tophead = ttk.Frame(self._headerframe, style="success.TFrame")
        self._appname = ttk.Label(self._tophead, text="Daily Todo", anchor="n", style="success.Inverse.TLabel",
                                  font=(self._font, 24, "bold"), padding=(WIDTH//5.5, 0, 0, 0))
        self._appname.pack(side="right", fill="x", expand=1)

        self._img = ImageTk.PhotoImage(Image.open(
            f"{path}/{'sun.png' if DARK else 'moon.png'}").resize((20, 20)))
        self._modebtn = ttk.Button(self._tophead, image=self._img, padding=(12),
                                   style="success.TButton", command=self._change_mode)
        self._modebtn.pack(side="right", before=self._appname)
        self._tophead.pack(side="top", fill="both", expand=1)

        self._headerframe.pack(side="top", fill="x")

    def _todo_area(self):
        """Main area of window where All todo's are displayed"""
        self._mainframe = ttk.Frame(self, style="danger.TFrame")
        # canvas will have frame which will be scrollable
        self._canvas = tk.Canvas(self._mainframe, background="gold")
        self._scrollbar = ttk.Scrollbar(self._mainframe, orient="vertical",
                                       command=self._canvas.yview)
        self._todoframe = ttk.Frame(self._canvas, style="success.TFrame")
        self.taskvars = []

        self._todoframe.bind("<Configure>", lambda e: self._canvas.configure(
                             scrollregion=self._canvas.bbox("all")))

        self._canvas.create_window(
            (0, 0), window=self._todoframe, width=WIDTH-10, anchor="nw")
        self._canvas.configure(yscrollcommand=self._scrollbar.set)

        # self._todoframe.pack(fill="both", expand=1)
        self._canvas.pack(side="left", fill="both", expand=1)
        self._scrollbar.pack(side="right", fill="y")

        self._mainframe.pack(side="top", fill="both", expand=1)

    def _footer(self):
        """Footer to create new Todo"""
        self._footerframe = ttk.Frame(self, style="info.TFrame")

        self._topfooter = ttk.Frame(self._footerframe, style="success.TFrame")
        self._newtask = tk.StringVar(self._topfooter, "Add new Task")
        self._addentry = ttk.Entry(self._topfooter, textvariable=self._newtask,
                                   font=(self._font, 12), state="readonly")
        self._addentry.pack(side="left", fill="x", expand=1)
        self._addentry.bind("<Button-1>", lambda e: e.widget.configure(state="active")
                            or self._newtask.set("") or self._addbtn.configure(state="active"))
        # if user is entering new task, mouse event will disabled
        self._addentry.bind("<KeyRelease>",
                            lambda e: e.widget.unbind(sequence="<Button-1>"))
        self._addentry.bind("<Return>", lambda e: self._add_task())

        self._addimg = ImageTk.PhotoImage(
            Image.open(f"{path}/add.png").resize((20, 21)))
        self._addbtn = ttk.Button(self._topfooter, image=self._addimg,
                                  state="disabled", style="success.TButton",
                                  command=self._add_task)
        self._addbtn.pack(side="left")
        self._topfooter.pack(side="top", fill="x", padx=50)

        self._progressbar = ttk.Progressbar(self._footerframe, maximum=100, value=25,
                                            style="warning.Horizontal.TProgressbar")
        self._progressbar.pack(side="top", fill="x", expand=1)
        self._footerframe.pack(side="bottom", fill="x")

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
        """Create a Task Frame"""
        _taskframe = ttk.Frame(self._todoframe, padding=(
            10, 2), style="success.TFrame")
        print(_taskframe, taskname, str(taskno))
        self._taskname = tk.StringVar(_taskframe, taskname, taskname)
        self.taskvars.append(self._taskname)
        _task = ttk.Entry(_taskframe, textvariable=self._taskname, font=(self._font, 12),
                          state="readonly", cursor="arrow", style="success.TEntry")
        _task.pack(side="left", fill="x", expand=1, padx=20)
        _taskframe.pack(side="top", fill="x")

        _taskframe.bind("<Enter>", lambda e: _taskframe.config(relief="solid"))
        _taskframe.bind("<Leave>", lambda e: _taskframe.config(relief="flat"))
        _task.bind("<Enter>", lambda e: _taskframe.config(relief="solid"))
        _task.bind("<Leave>", lambda e: _taskframe.config(relief="flat"))
        _task.bind("<Button-1>", self._edit_task)
        _task.bind("<Return>", lambda e: e.widget.config(state="readonly"))

    def _edit_task(self, event):
        """Edit the task"""
        old_task = event.widget["textvariable"]
        event.widget.config(state="active")
        if old_task == event.widget["textvariable"]:
            return

    def _change_mode(self):
        """Change night mode to day mode and vice-versa."""
        global DARK
        self._img = ImageTk.PhotoImage(Image.open(
            f"{path}/{'moon.png' if DARK else 'sun.png'}").resize((20, 20)))
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
