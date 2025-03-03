from tkinter.messagebox import showerror
from .base import BaseManager

class Updation_UI(BaseManager): 
    def __init__(self, master, widget):
        try:
            super().__init__(master, title="Update Widget")
        except Exception:
            showerror("Error", message=f"Instance of {self.master.title()} is running.", parent=self.master)
            return
        self.optionMENU(widget)
