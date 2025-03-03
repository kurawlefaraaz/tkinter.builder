
from tkinter import Toplevel, StringVar, BooleanVar, IntVar, Frame, Button, Label, Checkbutton, Spinbox
from tkinter.ttk import Combobox
from tkinter.font import Font, families, names

class SimpleFontChooser(Toplevel):
    
    def __init__(self, master, font="TkDefault", **options):
        """
        Create a new FontChooser instance.

        Arguments:

            master : Tk or Toplevel instance
                master window

            font : String

            text : str
                text to be displayed in the preview label

            title : str
                window title

            options : dict
                additional keyword arguments to be passed to ``Toplevel.__init__``
        """
        super().__init__(master, **options)
        self.grab_set()
        root = self.nametowidget(".")
        # --- family list
        self.font_list = list(set(families(root)).union(names(root)))
        self.font_list.sort()
        self.font_list = tuple(ele.replace(" ", "\\") for ele in self.font_list)

        del root

        font = font.split(" ")
        self.font = Font(self, family=font[0])
        for index, key in enumerate(font[1:], 1):
            if index == 1: self.font.configure(size= key)
            elif index == 2: self.font.configure(weight= key)
            elif index == 3: self.font.configure(slant= key)
            elif index == 4: self.font.configure(underline= 1)
            elif index == 5: self.font.configure(overstrike= 1)
        

        ### Font Family Select         
        self.font_family_option_selected = StringVar(self, self.font.cget('family'))
        family_menu = Combobox(self, textvariable=self.font_family_option_selected, values = self.font_list, height=10, state = 'readonly')
        family_menu.bind("<<ComboboxSelected>>", self.update_family)
        family_menu.grid(row=0, column=0, sticky="ew", pady=(10, 1), padx=(10, 0))

        ### Font Size Select
        self.font_size_selected = IntVar(self, self.font.cget('size'))
        font_size_spinbox = Spinbox(self, from_=0, textvariable=self.font_size_selected, to='infinity', command=self.update_size, state="readonly")
        
        font_size_spinbox.grid(row=0, column=1, sticky="ew",
                             pady=(10, 1), padx=(10, 0))

        ### Font Options
        options_frame = Frame(self, relief='groove', borderwidth=2)
        
        self.var_bold = BooleanVar(self, self.font.cget('weight') == "bold")
        b_bold = Checkbutton(options_frame, text="Bold", variable=self.var_bold, command=self.toggle_bold)
        b_bold.grid(row=0, column=0, padx=5)

        self.var_italic = BooleanVar(self, self.font.cget('slant') == "italic")
        b_italic = Checkbutton(options_frame, text="Italic", variable=self.var_italic, command=self.toggle_italic)
        b_italic.grid(row=0, column=1, padx=5)

        self.var_underline = BooleanVar(self, self.font.cget('underline'))
        b_underline = Checkbutton(options_frame, text="Underline", variable=self.var_underline, command=self.toggle_underline)
        b_underline.grid(row=0, column=2, padx=5)

        self.var_overstrike = BooleanVar(self, self.font.cget('overstrike'))
        b_overstrike = Checkbutton(options_frame, text="Overstrike", variable=self.var_overstrike, command=self.toggle_overstrike)
        b_overstrike.grid(row=0, column=3, padx=5)

        options_frame.grid_columnconfigure(0, weight=1)
        options_frame.grid_columnconfigure(1, weight=1)
        options_frame.grid_columnconfigure(2, weight=1)
        options_frame.grid_columnconfigure(3, weight=1)
        options_frame.grid(row=1, column=0, columnspan=2,
                           padx=10, pady=10, ipadx=10, sticky="ew")
    
        ### Preview Label
        text = "Quick brown fox jumped over the lazy dogs."
        self.preview = Label(self, relief="groove",
                             text=text, font=self.font,
                             anchor="center", background="white")
        self.preview.grid(row=2, column=0, columnspan=5, sticky="ew",
                          padx=10, pady=(0, 10), ipadx=4, ipady=4)
        
        ### Buttons
        button_frame = Frame(self)
        button_frame.grid(row=3, column=0, columnspan=2, pady=(0, 10), padx=10)
        Button(button_frame, text="Ok",
               command=self.ok_func).grid(row=0, column=0, padx=4, sticky='ew')
        Button(button_frame, text="Cancel",
               command=self.cancel_func).grid(row=0, column=1, padx=4, sticky='ew')
    
    def update_family(self, event):
        self.font.configure(family=self.font_family_option_selected.get())

    def update_size(self):
        self.font.configure(size = self.font_size_selected.get())

    def toggle_bold(self):
        """Update font preview weight."""
        b = self.var_bold.get()
        self.font.configure(weight=["normal", "bold"][b])

    def toggle_italic(self):
        """Update font font slant."""
        b = self.var_italic.get()
        self.font.configure(slant=["roman", "italic"][b])

    def toggle_underline(self):
        """Update font preview underline."""
        b = self.var_underline.get()
        self.font.configure(underline=b)

    def toggle_overstrike(self):
        """Update font preview overstrike."""
        b = self.var_overstrike.get()
        self.font.configure(overstrike=b)
    
    def cancel_func(self): 
        self.destroy()

    def ok_func(self): 
        super().destroy()

    def destroy(self):
        self.font = None
        return super().destroy()
    
    def get_result(self):
        return self.font

    def get_str_result(self):
        if not self.font: return None
        font = f"{self.font.cget("family")} {self.font.cget("size")} {self.font.cget("weight")} {self.font.cget("slant")}"
        if self.font['underline']:
            font += ' underline'
        if self.font['overstrike']:
            font += ' overstrike'
        
        return font
        
        
def askfont(master=None, text="Abcd", title="Font Chooser", font=None):
    """
    Open the font chooser and return a dictionary of the font properties.

    General Arguments:

        master : Tk or Toplevel instance
            master window

        text : str
            sample text to be displayed in the font chooser

        title : str
            dialog title

    Font arguments:

        family : str
            font family

        size : int
            font size

        slant : str
            "roman" or "italic"

        weight : str
            "normal" or "bold"

        underline : bool
            whether the text is underlined

        overstrike : bool
            whether the text is overstriked

    Output: Font Object

    """
    chooser = SimpleFontChooser(master, font)
    chooser.wait_window(chooser)
    return chooser.get_str_result()


if __name__ == "__main__":
    """Example."""
    from tkinter import Tk


    root = Tk()
    label = Label(root, text='Chosen font: ')
    label.pack(padx=10, pady=(10, 4))

    def callback():
        font = askfont(root, title="Choose a font: ", font="Times")
        print(font)
        if font:
            label.configure(font= font, text= f"Choose a font: {font}")

    Button(root, text='Font Chooser', command=callback).pack(padx=10, pady=(4, 10))
    root.mainloop()