from tkinter.ttk import Notebook, Frame, Label, Style
class DynamicNotebook(Notebook):
    def __init__(self, master):
        super().__init__(master)
        self.root = master
        self._tabDefualt= Frame
        self._tabDefualt_options = {"master": self}
        self.LAST_SELECTED_TAB = None
        self.counter = 1

    def setDefualtFrame(self, widget_class, **widget_class_options):
        self._tabDefualt_options = widget_class_options
        self._tabDefualt= widget_class

    def intialize_Frames(self):
        frame1 = self._tabDefualt(**self._tabDefualt_options)

        self.add(frame1, text="Frame", sticky="nsew")
        self.add(Label(self), text="-")
        self.add(Label(self), text="+")
        self.LAST_SELECTED_TAB = self.index("current")
        self.bind("<<NotebookTabChanged>>", self.watcher)

    def add_frame_button_func(self):
        c = self.index("current")
        self.insert_frame(c - 1)

    def insert_frame(self, index):
        tab_text = "Frame"
        frame = self._tabDefualt(**self._tabDefualt_options)
        
        self.insert(index, frame, text=tab_text, sticky="nsew")
        self.select(index)

    def remove_frame(self, index):
        self.forget(index)
        self.select(index)

    def get_current_frame_tcl_name(self):
        current_index = self.index("current")
        return self.root.nametowidget(self.tabs()[current_index])

    def watcher(self, e):
        tab_name = self.tab(self.select(), "text")
        current_tab_index = self.index("current")
        if tab_name not in ("-", "+"):
            self.LAST_SELECTED_TAB = current_tab_index
            return

        if tab_name == "-":
            if self.index("end") > 3:
                self.remove_frame(self.LAST_SELECTED_TAB)
            else:
                self.select(0)

        elif tab_name == "+":
            self.add_frame_button_func()