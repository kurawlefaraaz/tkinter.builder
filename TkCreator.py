import tkinter as tk
import tkinter.ttk as ttk
import traceback
from tkinter.messagebox import showerror

from UI import MethodWindow, Updation_UI

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.report_callback_exception = self.loud_exceptions
        self.wm_protocol("WM_DELETE_WINDOW", self.close)

        self.title("Workspace")
        self.saved_code = {}   
        s = ttk.Style(self)
        s.theme_use("clam")
        s.configure("TNotebook", background = "white")

        self.update()
        self.add_method_window()

    def call_update_ui(self, event):
        Updation_UI(self.nametowidget("method_window"), widget= event.widget)

    def add_method_window(self):
        MethodWindow(self)
        self.bind("<Button-3>", self.call_update_ui)

    def loud_exceptions(self, *args):
        err = traceback.format_exception(*args)
        err = err[-1].replace("_tkinter.TclError: ", "").title()
        showerror('Exception', err, parent=self)
    
    def close(self):
        self.report_callback_exception = lambda *args: None
        self.destroy()

if __name__ == "__main__":
    A = GUI()
    A.mainloop()
