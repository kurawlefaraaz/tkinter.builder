from tkinter.messagebox import showerror

from utilities import create_widget, on_new_widgets
from UI.widget_setup import GetWidgetSetupData
from .base import BaseManager


class Creation_UI(BaseManager):
    def __init__(self, master, widget_class):
        try:
            super().__init__(master, title = "Create Widget")
        except Exception:
            showerror("Error", message=f"Instance of {self.master.title()} is running.", parent=self.master)
            return
        master_name_data= GetWidgetSetupData(self)
        master_name_dict = master_name_data.get()

        if not master_name_dict: 
            self.close()
            return

        self.widget = create_widget(
            widget_class=widget_class,
            widget_master=master_name_dict.get("master"),
            widget_name=master_name_dict.get("name"),
        )
        on_new_widgets(self.widget)

        self.optionMENU(self.widget)
