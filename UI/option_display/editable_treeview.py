import tkinter as tk
import tkinter.ttk as ttk

class PopupEntry(tk.Toplevel):
    """
    Provides a temporary tk.Entry widget which can be used to show a temporaty entry widget to retrive data from user.
    After retriving data, it returns the value back and gets destroyed.

    Used internaly by EditableTreeview.
    """

    def __init__(
        self,
        master,
        x,
        y,
        width,
        height, def_value,
        **options
    ):  
        x += master.winfo_rootx()
        y += master.winfo_rooty()

        super().__init__(master)
        self.overrideredirect(1)
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.focusmodel("active")
        self.grab_set()
        
        self.textvar = tk.StringVar(self, def_value)
        
        entry = tk.Entry(self, textvariable=self.textvar, **options)
        entry.pack(fill="both", expand=1)
        entry.focus()
        entry.select_range(0, "end")
        entry.icursor("end")

        self._bind_widget()
        self.wait_window()
    
    def get(self):
        return self.textvar.get()
    
    
    def _bind_widget(self):
        self.bind("<Return>", self._exit)
        self.bind("<Button-1>", self._exit )
        self.master.bind("<MouseWheel>", lambda e: "break")

    def ring_bell(self, event):
        if event.widget is self: self.bell()

    def _exit(self, e=None):
        self.master.unbind("<MouseWheel>")
        self.destroy()
    
class EditableTreeview(ttk.Treeview):
    """Customized Treeview with editing feature

    All treeview attributes are valid"""

    def __init__(
        self,
        master,
        columns,
        show,
        data: tuple,
        bind_key="<Double-Button-1>",
        non_editable_columns="",
        name= None, 
        **treeview_options
    ):
        super().__init__(master, name=name, columns=columns, show=show, **treeview_options)
        self.column_name = columns
        self.data = data
        self.bind("<Double Button-1>" if bind_key == None else bind_key, self.edit)
        self.non_editable_columns = non_editable_columns

        self.set_headings()
        self.insert_data()
        self.update()
        self.event_add("<<RowUpdated>>", "<Map>")

        self.style = ttk.Style(self)

    def set_headings(self):
        for i in self.column_name:
            self.heading(column=i, text=i)

    def insert_data(self):
        for values in self.data:
            self.insert("", tk.END, values=values)

    def get_current_column(self, mouse_x):
        return self.identify_column(mouse_x)

    def get_cell_cords(self, row, column):
        return self.bbox(row, column=column)

    def get_selected_cell_cords(self, mouse_x):
        row = self.focus()
        column = self.get_current_column(mouse_x)
        return self.get_cell_cords(row=row, column=column)

    def update_row(self, values, iid):
        self.item(iid, values=values)

    def is_non_cell(self, mouse_x, mouse_y):
        result = self.identify_region(mouse_x, mouse_y)
        if result in ("heading", ):
            return True
        else:
            return False

    def is_non_editable(self, mouse_x):
        if self.get_current_column(mouse_x) in self.non_editable_columns:
            return True
        else:
            return False

    def show_popup_widget(self):
        new_val = PopupEntry(
            self,
            self.popup_x,
            self.popup_y,
            self.popup_w,
            self.popup_h,
            def_value=self.current_cell_value,
            font= self.style.lookup(self.cget("style"), "font")).get()
        
        return new_val
    
    def edit(self, e):
        if self.is_non_cell(e.x, e.y) or self.is_non_editable(e.x):
            return

        current_row = self.focus()
        self.current_row_values = list(self.item(current_row, "values"))

        current_column = int(self.get_current_column(e.x).replace("#", ""))
        self.current_cell_value = self.current_row_values[current_column-1]

        entry_cord = self.get_selected_cell_cords(e.x)
        self.popup_x = entry_cord[0]
        self.popup_y = entry_cord[1] 
        self.popup_w = entry_cord[2]
        self.popup_h = entry_cord[3] 

        new_val = self.show_popup_widget()

        if new_val != self.current_cell_value:
            self.current_row_values[current_column-1] = new_val

            self.update_row(
                values=self.current_row_values,
                iid= current_row
            )
            self.event_generate("<<RowUpdated>>")
        self.selection_set(current_row)

def demo():
    root = tk.Tk()
    root.title('Demo')
    root.geometry('620x200')
    
    columns = ('attribute', 'value', 'Broh')
    data = ((i,i) if i!=10 else (i,i,"test") for i in range(100))
    s = ttk.Style(root)
    s.configure("Treeview", font= "Courier 12")
    tree = EditableTreeview(root, columns=columns, show='headings',bind_key='<Double-Button-1>',data=data, non_editable_columns="#1")
    tree.pack()
    root.mainloop()

if __name__ == "__main__": demo()