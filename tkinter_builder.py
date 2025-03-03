import tkinter as tk
import tkinter.ttk as ttk
import traceback
from tkinter.messagebox import showerror, askyesno
from UI import MethodWindow, Updation_UI
from utilities import on_new_widgets

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.report_callback_exception = self.loud_exceptions

        self.title("Workspace")
        
        s = ttk.Style(self)
        s.theme_use("clam")
        
        self.module = "tk"
        self.widget_option_changed_dict = {}
        self.mgr_option_changed_dict = None 
        self.saved_code = {}
        self.scope = {}

        self.add_method_window()
        self.update()
        
        self.bind("<Map>", self.on_new_widget_map)

    def call_update_ui(self, event):
        if event.widget.winfo_name() == ".raise_method_window": return
        Updation_UI(self.nametowidget("method_window"), widget= event.widget)
        
    def add_method_window(self):
        self.method_window = MethodWindow(self)
        self.bind("<Button-3>", self.call_update_ui)
        self.widget_list.insert("", self)

    def loud_exceptions(self, *args):
        err = traceback.format_exception(*args)
        err = err[-1].replace("_tkinter.TclError: ", "").title()
        showerror('Exception', err, parent=self)
    
    def on_new_widget_map(self, e):
        if str(e.widget) in (".raise_method_window"): return
        on_new_widgets(e.widget)

    def destroy(self):
        confirm = askyesno("Warning", "Do you want to close main window?", parent=self)
        if confirm:
            self.report_callback_exception = lambda *args: None
            super().destroy()
