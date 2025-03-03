from tkinter.ttk import Notebook, Frame, Style
from tkinter import PhotoImage, StringVar, Entry

class DynamicNotebook(Notebook):
    __initialized = False

    def __init__(self, master):
        if not self.__initialized:
            self.__initialize_custom_style()
            self.__inititialized = True

        super().__init__(master, style="ClosableTabs.TNotebook")
        self.root = master
        self._tabDefualt= Frame
        self._tabDefualt_options = {"master": self}

        self._active = None
        self.count = 1
         
        self.bind("<Double-ButtonPress-1>", self.rename_tab)
        self.bind("<ButtonPress-1>", self.on_close_press, True)
        self.bind("<ButtonRelease-1>", self.on_close_release)

    def on_close_press(self, event):
        """Called when the button is pressed over the close button"""

        element = self.identify(event.x, event.y)
        if len(self.tabs()) == 1: return

        if "close" in element:
            index = self.index("@%d,%d" % (event.x, event.y))
            self.state(['pressed'])
            self._active = index
            return "break"

    def on_close_release(self, event):
        """Called when the button is released"""
        if not self.instate(['pressed']):
            return

        element =  self.identify(event.x, event.y)
        if "close" not in element:
            # user moved the mouse off of the close button
            return

        index = self.index("@%d,%d" % (event.x, event.y))

        if self._active == index:
            self.forget(index)
            self.event_generate("<<NotebookTabClosed>>")

        self.state(["!pressed"])
        self._active = None

    def __initialize_custom_style(self):
        """Code by @Bryan Oakley"""
        self.style = Style()
        self.images = (
            PhotoImage("img_close", data='''
                R0lGODlhCAAIAMIBAAAAADs7O4+Pj9nZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
                '''),
            PhotoImage("img_closeactive", data='''
                R0lGODlhCAAIAMIEAAAAAP/SAP/bNNnZ2cbGxsbGxsbGxsbGxiH5BAEKAAQALAAA
                AAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU5kEJADs=
                '''),
            PhotoImage("img_closepressed", data='''
                R0lGODlhCAAIAMIEAAAAAOUqKv9mZtnZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
            ''')
        )
        self.style.theme_use("clam")
        self.style.configure("ClosableTabs.TNotebook", background = "white")
        self.style.element_create("close", "image", "img_close",
                            ("active", "pressed", "!disabled", "img_closepressed"),
                            ("active", "!disabled", "img_closeactive"), border=8, sticky='')
        self.style.layout("ClosableTabs.TNotebook", [("ClosableTabs.TNotebook.client", {"sticky": "nswe"})])
        
        self.style.layout("ClosableTabs.TNotebook.Tab", [
            ("ClosableTabs.TNotebook.tab", {
                "sticky": "nswe",
                "children": [
                    ("ClosableTabs.TNotebook.padding", {
                        "side": "top",
                        "sticky": "nswe",
                        "children": [
                            ("ClosableTabs.TNotebook.focus", {
                                "side": "top",
                                "sticky": "nswe",
                                "children": [
                                    ("ClosableTabs.TNotebook.entry_anchor", {"side": "left", "sticky": ''}),
                                    ("ClosableTabs.TNotebook.label", {"side": "left", "sticky": ''}),
                                    ("ClosableTabs.TNotebook.close", {"side": "left", "sticky": ''}),
                                ]
                            })
                        ]
                    })
                ]
            })
        ])

    def setDefualtFrame(self, widget_class, **widget_class_options):
        self._tabDefualt_options = widget_class_options
        self._tabDefualt= widget_class

    def add_frame(self):
        tab_text = f"Frame{self.count}"
        frame = self._tabDefualt(**self._tabDefualt_options)
        
        self.add(frame, text=tab_text, sticky="nsew")
        self.count+=1

    def get_current_frame_tcl_name(self):
        current_index = self.index("current")
        return self.root.nametowidget(self.tabs()[current_index])
    
    def rename_tab(self, event):
        if not (self.identify(event.x, event.y) in ("padding", "tab") and self.identify(event.x+5, event.y) in ("label", "focus")):
            return 
        tab_name = self.tab("current", "text")

        rename_entry= Entry(self, width=len(tab_name), background="white")
        var = StringVar(rename_entry, tab_name)
        rename_entry["textvariable"] =  var

        rename_entry.focus()
        rename_entry.select_range(0, "end")
        rename_entry.icursor("end")

        rename_entry.bind("<Return>", lambda e: rename_entry.destroy())
        rename_entry.bind("<FocusOut>", lambda e: rename_entry.destroy())
        rename_entry.place(x=event.x, y=3)
        rename_entry.wait_window()
        
        new_name = var.get()
        if tab_name != new_name and new_name != "":
            self.tab("current", text=new_name)


if __name__ == "__main__":
    from tkinter import Tk
    root = Tk()
    a = DynamicNotebook(root)
    a.add_frame()
    a.pack(fill="both", expand=1)
    root.mainloop()