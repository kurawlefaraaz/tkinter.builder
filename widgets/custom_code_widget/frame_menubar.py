from tkinter import Frame, Menubutton, Menu
class FrameMenubar(Frame):
    """A workaround to achive a menubar that can be attached to a particular frame."""
    def __init__(self, master, **frame_options):
        super().__init__(master, **frame_options)

        self._menu_options = {}
        self._menu_button_pack_options = {}
    
    def addMenubutton(self, **menu_btn_options):
        menu_btn = Menubutton(self, **menu_btn_options)

        menu = Menu(menu_btn, **self._menu_options)
        menu_btn.config(menu=menu)

        menu_btn.pack(self._menu_button_pack_options)
        
        return menu
    
    def setMenuButtonPackOptions(self, **options):
        self._menu_button_pack_options = options

    def setMenuOptions(self, **options):
        self._menu_options = options