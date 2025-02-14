import tkinter as tk
import tkinter.ttk as ttk

class WidgetList(ttk.Treeview):
    def __init__(self, master):
        super().__init__(master, name="widget_list", selectmode="browse", show="tree")
        self.root = self.nametowidget('.')
        self.bind("<Double Button-1>", self.call_update_ui)
        self.heading('#0', text='Widget List', anchor="n")
    
    def call_update_ui(self, event):
        sel = self.focus()
        event.widget = self.nametowidget(sel)
        self.root.call_update_ui(event)

    def insert(self, parent, widget):
        widget_name = widget.winfo_name()
        super().insert(parent if parent else "", "end", iid=widget, text=widget_name)
    
    def delete(self, widget):
        super().delete(widget)
    
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