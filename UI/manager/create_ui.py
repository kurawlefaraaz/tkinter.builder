from utilities import create_widget
from UI.widget_setup import GetWidgetSetupData
from .base import BaseManager


class Creation_UI(BaseManager):
    def __init__(self, master, widget_class):
        super().__init__(master, title = "Create Widget")

        widget_scope = {}

        master_name_data= GetWidgetSetupData(self)
        master_name_dict = master_name_data.get()
        if not master_name_dict: 
            self.close()
            return

        self.widget = create_widget(
            widget_class=widget_class,
            widget_master=master_name_dict.get("master"),
            widget_name=master_name_dict.get("name"),
            # widget_manager="place",
            # manager_options={'x': 0, 'y': 0},
        )
        self.widget.scope = widget_scope

        self.optionMENU(self.widget)
