import tkinter as tk

from .dynamic_notebook import DynamicNotebook
from .menubar import Menubar
from .numbered_text import NumberedText
from .console_output_text import ReadOnlyConsole

class ExecuteCodeFrame(tk.LabelFrame):
    def __init__(self, master, widget, **options) -> tk.LabelFrame:
        super().__init__(master, **options)

        self.root = self.nametowidget(".")
        self.widget= widget

        self.menubar = Menubar(self, self.widget)
        if master.winfo_class() == "TNotebook": self.menubar.notebook_menu()

        pane = tk.PanedWindow(self, orient= "vertical", showhandle=1, sashpad=10, sashwidth=10, sashrelief='ridge', opaqueresize=0, background="white")

        self.textbox = NumberedText(master=pane)
        # self.textbox.pack(padx=20, pady=5, fill="x")
        pane.add(self.textbox, padx=10, pady=10, height=500)

        console = ReadOnlyConsole(master=pane)
        pane.add(console, padx=10, pady=10, height=200)

        pane.pack(padx=20, pady=5, fill="both")

class ExecuteCode(DynamicNotebook):
    def __init__(self, master, widget, **options):
        super().__init__(master)
        self.setDefualtFrame(ExecuteCodeFrame, master=self, widget=widget, **options)
        self.add_frame()

def demo():
    root = tk.Tk()
    a=ExecuteCode(root)
    a.pack()
    root.mainloop()

if __name__ == "__main__":
    demo()