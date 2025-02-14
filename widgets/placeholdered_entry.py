import tkinter as tk

class PlaceholderedEntry(tk.Entry):
    def __init__(self, master=None, placeholder= "", **options):
        self.placeholder = placeholder
        super().__init__(master, **options)

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)
        self.add_placeholder()
        
    def add_placeholder(self):
        self.insert(0, self.placeholder)

    def foc_in(self, event): 
        self.delete(0, len(self.placeholder))
            
    def foc_out(self, event): 
        self.add_placeholder()