import tkinter as tk
from tkinter.colorchooser import askcolor
from tkinter.filedialog import askopenfile

from widgets import askfont

from .editable_treeview import EditableTreeview

class PopupEntry(tk.Entry):
    """
    Provides a temporary tk.Entry widget which can be used to show a temporaty entry widget to retrive data from user.
    After retriving data, it returns the value back and gets destroyed.

    Used internaly by EditableTreeview.

    """

    def __init__(
        self,
        parent,
        x,
        y,
        width,
        height,
        def_value="",
        **options
    ):
        super().__init__(
            parent,
            relief="flat",
            justify="left",
            bg="white",
            highlightthickness=2,
            highlightbackground="grey",
            **options
        )
        self.textvar = tk.StringVar(self, def_value)
        self.configure(textvariable=self.textvar)
        self.place(x=x + 1, y=y, width=width, height=height)

        method_w = self.nametowidget(".").method_window
        method_w.wm_protocol("WM_DELETE_WINDOW", "break")

        self.focus_set()
        self.grab_set()
        self.select_range(0, "end")
        # move cursor to the end
        self.icursor("end")

        self._bind_widget()
        self.wait_window()
        method_w.wm_protocol("WM_DELETE_WINDOW", method_w.withdraw)

    def _bind_widget(self):
        self.bind("<Return>", lambda e: self.destroy())
        self.bind("<Button-1>", lambda e: self.destroy())

    def get(self):
        return self.textvar.get()

    def _indicate_widget_visible(self, e):
        self.bell()
        
        for i in range(2):
            print(1)
            self.configure(highlightcolor="red")
            self.update()
            self.after(100)
            print(2)
            self.configure(highlightcolor="grey")
    
class OptionTreeview(EditableTreeview):
    def __init__(
        self,
        master,
        name=None,
        data: dict = {},
        **treeview_options
    ):  
        data = data.items()
        super().__init__(master, name=name, columns=("Attribute", "Value"), show="headings", data=data, non_editable_columns="#1", **treeview_options)

        yscrollbar = tk.Scrollbar(self.master, relief="flat", background="white", command=self.yview) 
        yscrollbar.pack(side="right", fill="y")
        
        self.configure(yscrollcommand = yscrollbar.set)
        self.column("#1", stretch=0)
    
    def show_popup_widget(self):
        attr = self.current_row_values[0]
        c_value = self.current_cell_value

        if "background" in attr or "foreground" in attr or "color" in attr:
            new_val = askcolor(c_value, parent=self)[1]

            if new_val:return new_val
            else: return c_value 
        elif attr == "font":
            new_val = askfont(self, font=c_value)
            
            if new_val:return new_val
            else: return c_value 
        elif attr in ("image", "menu", "cursor", "bitmap", "buttoncursor") or "variable" in attr:
            PopupEntry(self, 
                self.popup_x,
                self.popup_y,
                self.popup_w,
                self.popup_h,
                "Change by Code Execution Only",
                font=self.style.lookup(self.cget("style"), "font"), 
                state= "readonly")
            return c_value
        elif attr in ("path", "class", "widget_code", "manager_code", "name", "master"):
            PopupEntry(self, 
                self.popup_x,
                self.popup_y,
                self.popup_w,
                self.popup_h,
                c_value,
                font=self.style.lookup(self.cget("style"), "font"), 
                state= "readonly")
            return c_value
        else:
            return PopupEntry(self, 
                self.popup_x,
                self.popup_y,
                self.popup_w,
                self.popup_h,
                c_value,
                font=self.style.lookup(self.cget("style"), "font")).get()
        
def demo():
    root = tk.Tk()
    root.title('Demo')
    
    data = dict((i, i) if i!=10 else ("background", "#000000") for i in range(100))

    tree = OptionTreeview(root, data=data)
    tree.pack()

    root.mainloop()

if __name__ == "__main__": demo()