from tkinter import Frame, PanedWindow
from tkinter.messagebox import showerror

from widgets import ExecuteCodeFrame, BorderedButton
from utilities import get_widget_code, get_mgr_code

from ..option_display import WidgetOption, ManagerOption, WidgetMetadata

class BaseManager(Frame):
    def __init__(self, master, title) -> Frame:
        super().__init__(master, background="white")
        if self.master.title() != "Widget Catalog": 
            showerror("Error", message=f"Instance of {self.master.title()} is running.", parent=self.master)
            return 
        
        self.master.lift()
    
        self.master.resizable(1, 1)
        self.master.title(title)

        self.master.nametowidget("widget_catalog").pack_forget()
        self.pack(fill="both", expand=1)

    def optionMENU(self, widget):
        self.master.wm_protocol("WM_DELETE_WINDOW", lambda: self.delete_btn_func(widget))
        self.master.transient("")

        master_name_path_code_dict = {"master": widget.winfo_parent(), "name": widget.winfo_name(),'path': widget._w, "widget_code": get_widget_code(widget)}
        if widget.mgr_option_changed_dict != None:
            master_name_path_code_dict.update({"manager_code": get_mgr_code(widget)})

        main_pane = PanedWindow(self, orient= "horizontal", showhandle=1, sashpad=10, sashwidth=10, sashrelief='ridge', opaqueresize=0, background="white")
        
        left_frame = Frame(main_pane, background="white")

        main_pane.add(left_frame, padx=10, pady=10)

        widget_metadata = WidgetMetadata(
            master=left_frame,
            widget=widget,
            text="Widget Metadata",
            metadata=master_name_path_code_dict,
            background = "white")
        widget_metadata.pack(anchor="nw", fill="x")
        
        button_frame = Frame(left_frame, background="white")
        submit_button = BorderedButton(button_frame, text="Submit", command=self.close)
        submit_button.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        delete_button = BorderedButton(button_frame, text="Delete", command=lambda :self.delete_btn_func(widget))
        delete_button.grid(row=0, column=1, sticky="ew", padx=20, pady=10)
        button_frame.pack(anchor="n")

        widget_option = WidgetOption(
            master=left_frame,
            widget=widget,
            text="Widget Options",
            background = "white",
        )
        widget_option.pack(anchor="nw", fill="x")

        right_pane = PanedWindow(main_pane, orient="vertical", showhandle=1, sashpad=10, sashwidth=10, sashrelief='solid', opaqueresize=0, background="white")

        if widget.mgr_option_changed_dict != None:
            mgr_option = ManagerOption(
                master=right_pane,
                widget=widget,
                text="Manager Options",
                background = "white",
            )
            right_pane.add(mgr_option)
        
        custom_code_area = ExecuteCodeFrame(right_pane, text="Custom Code Block", background= "white",
            widget=widget)
        right_pane.add(custom_code_area, height=200)

        main_pane.add(right_pane)
        main_pane.pack(anchor="ne", fill="both", expand=1)

    def delete_btn_func(self, widget):
        self.close()
        self.nametowidget('.').widget_list.delete(widget)
        widget.destroy()

    def close(self): 
        self.master.title("Widget Catalog") # Title is used to check if an instance of Creation_UI or Update_UI is open, so once submit is pressed, title is reseted
        self.pack_forget()
        self.master.state("normal")
        self.master.geometry("")
        self.master.wm_protocol("WM_DELETE_WINDOW", self.master.withdraw)
        self.master.resizable(0, 0)
        self.master.nametowidget("widget_catalog").pack(fill="x")
        self.nametowidget('.').lift()
        self.master.lift()
        self.master.transient(self.master.master)
        self.destroy()