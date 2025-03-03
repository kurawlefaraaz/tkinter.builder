import tkinter as tk
import tkinter.ttk as ttk
from utilities import on_new_widgets

class WidgetList(ttk.Treeview):
    def __init__(self, master):
        super().__init__(master, name="widget_list", selectmode="browse", show="tree")
        self.root = self.nametowidget('.')
        self.bind("<Double Button-1>", self.call_update_ui)
        self.heading('#0', text='Widget List', anchor="n")
        
        self.root.widget_list = self
    
    def call_update_ui(self, event):
        sel = self.focus()
        event.widget = self.nametowidget(sel)
        self.root.call_update_ui(event)

    def insert(self, parent, widget):
        widget_name = widget.winfo_name()
        super().insert(parent if parent else "", "end", iid=widget, text=widget_name)
    
    def delete(self, widget):
        super().delete(widget)
    
    def get_children(self, item = None):
        return super().get_children(item)

    def refresh_widget_list(self):
        self.get_all_widgets(self.root)
    
    def get_all_widgets(self, master):
        if not master: return

        for child in master.winfo_children():
            if child.winfo_name() in ("method_window", "raise_method_window"): continue

            try: 
                self.insert(child.winfo_parent(), child)
                on_new_widgets(child)
                self.get_all_widgets(child)
            except: pass

    
if __name__=="__main__":
    root = tk.Tk()
    ttk.Style().theme_use("clam")
    wl = WidgetList(root)
    wl.insert(None, root)
    wl.pack()
    a = tk.Button(root, )
    wl.insert(root, a)
    delete_btn = tk.Button(root, )
    wl.insert(root, delete_btn)
    a = tk.Button(root, )
    wl.insert(root, a)
    a = tk.Button(root, )
    wl.insert(root, a)

    frame = tk.Frame(root)
    wl.insert(root, frame)

    a = tk.Label(frame, name= "hello_world", text="hello")
    wl.insert(frame, a)
    wl.after(7000, lambda: wl.delete(delete_btn))
    wl.after(7000, lambda: wl.delete(root))
    a = tk.Button(frame, name= "test_button", text="hello")
    wl.insert(frame, a)
    
    root.mainloop()