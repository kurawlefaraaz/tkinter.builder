import tkinter as tk

class Attributes:
    def __init__(self, widget) -> None:
        self.widget = widget

    def retrive_widget_attributes(self) -> dict:
        remove_attributes_tuple = ("class", "colormap", "container", "visual", "bg", "bd", "fg", "screen", "use", )
        
        attribute = self.widget.keys()
        attribute_value = [f"{self.widget.cget(i)}" for i in attribute]
        attributes_dict = dict(zip(attribute, attribute_value))
        
        ### Remove Some Attributes
        for key in remove_attributes_tuple: attributes_dict.pop(key, None)
        
        return attributes_dict

    def retrive_pack_attributes(self) -> dict:
        if self.widget.winfo_manager() != "pack":
            try:
                self.widget.pack()
            except Exception as exception:
                # Grid is already used to manage master's child
                return

        pack_attributes = self.widget.pack_info()

        return pack_attributes

    def retrive_grid_attributes(self) -> dict:

        if self.widget.winfo_manager() != "grid":
            try:
                self.widget.grid()
            except Exception as exception:
                # Pack is already used to manage master's child
                return

        grid_attributes = self.widget.grid_info()

        return grid_attributes

    def retrive_place_attributes(self) -> dict:
        if self.widget.winfo_manager() != "place":
            self.widget.place(x=0, y=0)

        place_attributes = self.widget.place_info()   

        return place_attributes
    
def create_widget(
        widget_class,
        widget_name:str, 
        widget_master,
    ):  
    w =widget_class(widget_master, name= widget_name)

    if w.winfo_class().startswith("T") and widget_class != "Tk":
        w.module = "ttk"
    else:
        w.module = "tk"

    w.widget_option_changed_dict = {}
    w.saved_code = {}
    w.nametowidget('.').widget_list.insert(widget_master, w)

    if w.winfo_class() not in ("tk", "Menu"):
        w.mgr_option_changed_dict = {}
        w.place(x=0, y=0)
    else:
        w.mgr_option_changed_dict = None

    return w

def get_widget_code(widget):
    widget_class = widget.winfo_class()
    master = widget.winfo_parent()
    name = widget.winfo_name()
    var_name = name.replace("!", "")

    widget_attrs_code = ", ".join((f'{key}= "{value}"' for key, value in widget.widget_option_changed_dict.items()))
    if master == ".": 
        master_name = "root"
    else: 
        master_name = widget.nametowidget(master).winfo_name()
        
    if widget.module == "ttk": widget_class = widget_class[1:]

    widget_CODE = f'''{var_name} = {widget.module}.{widget_class}({master_name}, name= "{name}", {widget_attrs_code})'''
    print(widget_CODE)

    return widget_CODE
def get_mgr_code(widget):
    name = widget.winfo_name()
    var_name = name.replace("!", "")
    mgr = widget.winfo_manager()
    mgr = mgr if mgr not in ("wm", "") else None
    
    if not mgr:
        return None

    mgr_attrs_code = ", ".join((f'{key}= "{value}"' for key, value in widget.mgr_option_changed_dict.items()))
    mgr_CODE = f"{var_name}.{mgr}({mgr_attrs_code})" if mgr else None
    return mgr_CODE
    
def demo():
    root = tk.Tk()

    widget = tk.Label(root)
    widget.pack()
    frame = tk.Frame(root)

    a = Attributes(frame)
    a.retrive_widget_attributes()
    a.retrive_pack_attributes()
    a.retrive_grid_attributes()
    a.retrive_place_attributes()
    print(a.widget_to_code())


if __name__ == "__main__":
    demo()
