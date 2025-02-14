from .base import BaseManager

class Updation_UI(BaseManager): 
    def __init__(self, master, widget):
        super().__init__(master, title="Update Widget")
        self.optionMENU(widget)
