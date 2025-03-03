import tkinter as tk


def retrive_widget_attributes(widget) -> dict:
    remove_attributes_tuple = ("class", "colormap", "container", "visual", "bg", "bd", "fg", "screen", "use", )
    
    attributes_dict = {option:str(value[-1]) for option, value in widget.configure().items() if option not in remove_attributes_tuple}
    return attributes_dict

def retrive_pack_attributes(widget) -> dict:
    if widget.winfo_manager() != "pack":
        try:
            widget.pack()
        except Exception as exception:
            # Grid is already used to manage master's child
            return

    pack_attributes = widget.pack_info()

    return pack_attributes

def retrive_grid_attributes(widget) -> dict:

    if widget.winfo_manager() != "grid":
        try:
            widget.grid()
        except Exception as exception:
            # Pack is already used to manage master's child
            return

    grid_attributes = widget.grid_info()

    return grid_attributes

def retrive_place_attributes(widget) -> dict:
    if widget.winfo_manager() != "place":
        widget.place(x=0, y=0)

    place_attributes = widget.place_info()   

    return place_attributes
    
def create_widget(
        widget_class,
        widget_master,
        widget_name:str, 
        **options
    ):  

    widget =widget_class(widget_master, name= widget_name, **options)

    return widget

def get_defaults(widget):
    wclass = widget.__class__
    mgr = widget.winfo_manager()

    if wclass != tk.OptionMenu:
        wclass = wclass()
    else: 
         wclass = wclass(None, None, None)
        
    result = (retrive_widget_attributes(wclass), globals()[f"retrive_{mgr}_attributes"](wclass) if wclass.winfo_class() not in ("tk", "Menu") else None)

    wclass.destroy()

    return result
    
def get_widget_code(widget):
    widget_class = widget.winfo_class()
    master = widget.winfo_parent()
    name = widget.winfo_name()
    var_name = name.replace("!", "")

    widget_attrs_code = ", ".join((f'{key}= "{value}"' for key, value in widget.widget_option_changed_dict.items()))
    if name == "tk":
        widget_CODE = "root = tk.Tk()\n"
        return widget_CODE
    if master == ".": 
        master_name = "root"
    else: 
        master_name = widget.nametowidget(master).winfo_name()
        
    if widget.module == "ttk": widget_class = widget_class[1:]

    widget_CODE = f'''{var_name} = {widget.module}.{widget_class}({master_name}, name= "{name}", {widget_attrs_code})\n'''

    return widget_CODE

def get_mgr_code(widget):
    name = widget.winfo_name()
    var_name = name.replace("!", "")
    mgr = widget.winfo_manager()
    mgr = mgr if mgr not in ("wm", "") else None
    
    if not mgr:
        return None

    mgr_attrs_code = ", ".join((f'{key}= "{value}"' for key, value in widget.mgr_option_changed_dict.items()))
    mgr_CODE = f"{var_name}.{mgr}({mgr_attrs_code})\n" if mgr else None
    return mgr_CODE
    
def attr_checker(widget):
    if hasattr(widget, "module"): return
    
    if widget.winfo_class().startswith("T") and widget.winfo_class() != "Tk":
        widget.module = "ttk"
    else:
        widget.module = "tk"

    widget.widget_option_changed_dict = {}
    widget.saved_code = {}
    widget.scope = {}
    
    if widget.winfo_class() not in ("tk", "Menu"):
        widget.mgr_option_changed_dict = {}
    else:
        widget.mgr_option_changed_dict = None

def new_configure(widget, cnf=None, **options):
    widget.widget_option_changed_dict.update(options)
    return_options = widget.old_configure(cnf, **options)
    widget.event_generate("<Configure>")
    return return_options

from types import MethodType
def on_new_widgets(widget):
    attr_checker(widget)

    if not widget.winfo_manager() and widget.winfo_class() not in ("tk", "Menu"):
        widget.place(x=0, y=0)

    default_widget_attr_dict, default_mgr_attr_dict = get_defaults(widget)

    changed_widged_attr_dict = {option: value for option, value in retrive_widget_attributes(widget).items() if default_widget_attr_dict.get(option) != value}

    if default_mgr_attr_dict:
        if default_mgr_attr_dict.get("x"): default_mgr_attr_dict.update({"x":None, "y":None})
        mgr_info = globals()[f"retrive_{widget.winfo_manager()}_attributes"](widget)
        changed_mgr_attr_dict = {option: value for option, value in mgr_info.items() if default_mgr_attr_dict.get(option) != value}

    try:
        widget.nametowidget('.').widget_list.insert(widget.winfo_parent(), widget)

        c = MethodType(new_configure, widget)
        
        widget.old_configure = widget.configure
        widget.old_config = widget.configure

        widget.configure = c
        widget.config = c

        widget.widget_option_changed_dict.update(changed_widged_attr_dict)
        widget.mgr_option_changed_dict.update(changed_mgr_attr_dict)
    except: pass


            
