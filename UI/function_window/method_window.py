from tkinter import Toplevel, Button

from .menubar import MenuBar
from .widgetcatalog import WidgetCatalog

class MethodWindow(Toplevel):
    def __init__(self, master):
        super().__init__(master, name="method_window", background="white")
        self.wm_protocol("WM_DELETE_WINDOW", self.withdraw)
        self.transient(master)
        self.resizable(0, 0)

        MenuBar(self)

        self.catalog = WidgetCatalog(self)
    
    def deiconify(self):
        self.nametowidget('.').nametowidget("raise_method_window").destroy()
        self.update()
        super().deiconify()
    
    def withdraw(self):
        super().withdraw()
        Button(self.master, name= "raise_method_window", text=self.title(), font="courier 7 bold",command=self.deiconify, anchor="n").place(x=0, y=0, relx=0,rely=1, anchor="sw")