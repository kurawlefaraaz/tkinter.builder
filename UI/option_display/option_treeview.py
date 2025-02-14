import tkinter as tk
from tkinter.colorchooser import askcolor

from .editable_treeview import EditableTreeview

class OptionTreeview(EditableTreeview):
    def __init__(
        self,
        master,
        name=None,
        data: dict = {},
        **treeview_options
    ):  
        data = data.items()
        super().__init__(master, name=name, columns=("Attribute", "Value"), show="headings", data=data, non_editable_columns="#1",**treeview_options)
    
    def show_popup_widget(self):
        if self.current_row_values[0] in ("background", "foreground"):
            return askcolor("#ffffff")[1]
        else:
            return super().show_popup_widget()
        
def demo():
    root = tk.Tk()
    root.title('Demo')
    
    data = dict((i, i) if i!=10 else ("background", "#000000") for i in range(100))

    tree = OptionTreeview(root, data=data)
    tree.pack()

    root.mainloop()

if __name__ == "__main__": demo()