from tkinter import Frame, PanedWindow, Scrollbar

from widgets import ExecuteCodeFrame, BorderedButton
import utilities

from ..option_display import WidgetOption, ManagerOption, WidgetMetadata

class BaseManager(Frame):
    def __init__(self, master, title) -> Frame:
        super().__init__(master, background="white")
        
        if master.title() != "Widget Catalog": 
            raise Exception(f"Instance of {self.master.title()} is running.")
        
        self.master.lift()
    
        self.master.resizable(1, 1)
        self.master.title(title)

        self.master.nametowidget("widget_catalog").pack_forget()
        self.pack(fill="both", expand=1)

    def optionMENU(self, widget):
        self.master.wm_protocol("WM_DELETE_WINDOW", lambda: self.delete_btn_func(widget))
        self.master.transient("")

        utilities.attr_checker(widget) # useful when importing projects

        master_name_path_code_dict = {"class": widget.winfo_class(), "master": widget.winfo_parent(), "name": widget.winfo_name(),'path': widget._w, "widget_code": utilities.get_widget_code(widget)}
        if widget.mgr_option_changed_dict != None:
            master_name_path_code_dict.update({"manager_code": utilities.get_mgr_code(widget)})

        main_pane = PanedWindow(self, orient= "horizontal", showhandle=1, sashpad=10, sashwidth=10, sashrelief='ridge', opaqueresize=0, background="white")
        
        left_frame = Frame(main_pane, background="white")

        widget_metadata = WidgetMetadata(
            master=left_frame,
            widget=widget,
            text="Widget Metadata",
            metadata=master_name_path_code_dict,
            background = "white")
        widget_metadata.tree.column("#1", width=150)
        widget_metadata.pack(anchor="nw", fill="x")
        
        button_frame = Frame(left_frame, background="white")
        submit_button = BorderedButton(button_frame, text="Submit", command=lambda: self.close(widget))
        submit_button.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        delete_button = BorderedButton(button_frame, text="Delete", command=lambda: self.delete_btn_func(widget))
        delete_button.grid(row=0, column=1, sticky="ew", padx=20, pady=10)
        button_frame.pack(anchor="n")

        widget_option = WidgetOption(
            master=left_frame,
            widget=widget,
            text="Widget Options",
            background = "white",
        )
        widget_option.tree.column("#1", width=250)
        widget_option.pack(anchor="nw", fill="x")

        main_pane.add(left_frame, padx=10, pady=10, height=600)

        right_pane = PanedWindow(main_pane, orient="vertical", showhandle=1, sashpad=10, sashwidth=10, sashrelief='solid', opaqueresize=0, background="white")

        if widget.mgr_option_changed_dict != None:
            mgr_option = ManagerOption(
                master=right_pane,
                widget=widget,
                text="Manager Options",
                background = "white",
            )
            mgr_option.tree.column("#1", width=150)
            right_pane.add(mgr_option, height=400)
        
        custom_code_area = ExecuteCodeFrame(right_pane, text="Custom Code Block", background= "white",
            widget=widget)
        right_pane.add(custom_code_area)

        main_pane.add(right_pane, width=400, height=600)
        main_pane.pack(anchor="ne", fill="both", expand=1)

    def delete_btn_func(self, widget):
        self.close(widget=widget)
        widget.destroy()
        if not widget.winfo_exists():
            self.nametowidget('.').widget_list.delete(widget)

    def close(self, widget=None): 
        self.master.title("Widget Catalog") # Title is used to check if an instance of Creation_UI or Update_UI is open, so once submit is pressed, title is reseted
        self.master.state("normal")
        self.master.geometry("")
        self.master.wm_protocol("WM_DELETE_WINDOW", self.master.withdraw)
        self.master.resizable(0, 0)
        self.master.lift()
        self.master.transient(self.master.master)
        self.master.nametowidget("widget_catalog").pack(fill="x")
        self.master.nametowidget("widget_catalog").reinvoke_enable_button()

        self.pack_forget()

        self.nametowidget('.').lift()
        
        if widget: widget.unbind("<Configure>")

        self.destroy()