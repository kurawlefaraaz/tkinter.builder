import tkinter as tk
from tkinter.ttk import Style

from .option_treeview import OptionTreeview
import utilities

class OptionDisplay(tk.LabelFrame):
    def __init__(self, master, widget, **options):
        super().__init__(master, **options)

        s= Style(self)
        s.configure("Treeview", font="Courier 12")
        s.configure("Big.Treeview", rowheight= 50, font="Courier 15")
        
        self.widget = widget

class WidgetMetadata(OptionDisplay):
    def __init__(self, master, widget, metadata,**options):
        super().__init__(master, widget, global_dict=None, **options)
        
        self.tree = OptionTreeview(self, name="meta_data_treeview", data={})
        for key, value in metadata.items():
            self.tree.insert("", "end", key, values=(key, value))
        self.tree.pack(fill="x")
        
        self.widget.bind("<Configure>", self.update_widget_code)
        if len(self.tree.get_children()) == 6:
            self.widget.bind("<Configure>", self.update_mgr_code, "+")
    
    def update_widget_code(self, e): 
        values = ("widget_code", utilities.get_widget_code(self.widget))
        self.tree.update_row(values=values, iid = self.tree.item("widget_code", "values")[0])

    def update_mgr_code(self, e):
        values = ("manager_code", utilities.get_mgr_code(self.widget))
        self.tree.update_row(values=values, iid = self.tree.item("manager_code", "values")[0])

class WidgetOption(OptionDisplay):
    def __init__(self, master, widget, **options):
        super().__init__(master=master, widget=widget, **options)
    
        data = utilities.retrive_widget_attributes(widget)
        self.tree = OptionTreeview(
            self,
            data=data,
            style="Big.Treeview",
            name="option_menu_treeview"
        )
        self.tree.pack(fill="x")
        
        self.tree.bind("<<RowUpdated>>", self.update_widget_option)
    
    def update_widget_option(self, event):
        option_changed = self.tree.item(self.tree.focus(), "values")
        
        if option_changed:
            option_changed = {option_changed[0]: option_changed[1]}
        else: option_changed = {}

        self.widget.configure(option_changed)
        self.widget.widget_option_changed_dict.update(option_changed)
        self.widget.event_generate("<Configure>")
            
class ManagerOption(OptionDisplay):
    def __init__(self, master, widget, **options):
        super().__init__(master, widget, **options)

        self.manager_types_frame()

        self.tree = OptionTreeview(
            self,
            data={},
            style="Big.Treeview",
            name="mgr_option_treeview"
        )
        self.tree.pack(fill="x", padx=20, pady=20)
        self.manager_select()
        self.tree.bind("<<RowUpdated>>", self.update_manager_option)

    def manager_types_frame(self):
        button_frame = tk.LabelFrame(self, text="Select Widget Manager", background="white")
        button_frame.pack(
            anchor="n",
            padx=10,
            pady=10,
        )

        self.RadioSelectedVar = tk.StringVar(self)

        selected_place = tk.Radiobutton(
            button_frame,
            text="Place",
            value="place",
            background="white",
            variable=self.RadioSelectedVar,
            command=self.update_manager,
        )
        selected_place.pack(side="left", padx=10, pady=5, anchor="w", expand=0)

        selected_grid = tk.Radiobutton(
            button_frame,
            text="Grid",
            value="grid",
            variable=self.RadioSelectedVar,
            background="white",
            command=self.update_manager,
        )
        selected_grid.pack(side="left", padx=10, pady=5, anchor="center", expand=0)

        selected_pack = tk.Radiobutton(
            button_frame,
            text="Pack",
            value="pack",
            variable=self.RadioSelectedVar,
            background="white",
            command=self.update_manager,
        )
        selected_pack.pack(side="left", padx=10, pady=5, anchor="e", expand=0)

    def manager_select(self):
        manager = self.widget.winfo_manager()
        if manager:
            self.RadioSelectedVar.set(manager)
        else:
            self.RadioSelectedVar.set("place")
        self.update_manager()

    def update_manager(self):
        rows = self.tree.get_children()
        for item in rows:
            self.tree.delete(item)

        manager_attributes = getattr(
            utilities, f"retrive_{self.RadioSelectedVar.get()}_attributes"
        )(self.widget)

        self.widget.mgr_option_changed_dict.clear()
        if self.RadioSelectedVar.get() == "place": self.widget.mgr_option_changed_dict.update(x=0, y=0)
        if manager_attributes != None:
            self.enable_treeview()
            for value in manager_attributes:
                self.tree.insert("", tk.END, values=(value, manager_attributes.get(value)))    
            self.widget.event_generate("<Configure>")
        else:
            self.tree.insert("", tk.END, values=("Error", f"Can not use geometry manager"))
            self.tree.insert("", tk.END, values=("Error", f"{self.RadioSelectedVar.get()} along with {'pack' if self.RadioSelectedVar.get() == 'grid' else 'grid'}"))
            self.disable_treeview()

    def disable_treeview(self):
        self.tree.state(("disabled",))
        self.tree.bind('<Button-1>', lambda e: 'break')

    def enable_treeview(self):
        self.tree.state(("!disabled",))
        self.tree.unbind('<Button-1>')
    
    def update_manager_option(self, event):
        option_changed = self.tree.item(self.tree.focus(), "values")
        if option_changed:
            option_changed = {option_changed[0]: option_changed[1]}
        else: option_changed = {}

        getattr(self.widget, self.widget.winfo_manager())(option_changed)
        self.widget.mgr_option_changed_dict.update(option_changed)
        self.widget.event_generate("<Configure>")
