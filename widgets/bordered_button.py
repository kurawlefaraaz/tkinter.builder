import tkinter as tk

class BorderedButton(tk.Button):
    def __init__(self, master, name=None, text="", command=None, font=None):
        self.border_frame = tk.Frame(master, highlightthickness=2, borderwidth=0)

        super().__init__(self.border_frame, name=name, text=text, command=command,  borderwidth=0, border=0, width=20, padx=0, pady=0, relief="flat", font=font)
        self.set_colors()
        super().pack()

        text_meths = vars(tk.Button).keys()
        methods = vars(tk.Pack).keys() | vars(tk.Grid).keys() | vars(tk.Place).keys()
        methods = methods.difference(text_meths)

        for m in methods:
            if m[0] != '_' and m != 'config' and m != 'configure':
                setattr(self, m, getattr(self.border_frame, m))
    
    def set_colors(self, background= "white", foreground= "#524d4d", disabledforeground="#c8c8c8"):
        activeforeground = background
        activebackground = foreground
        border_color = foreground

        self.configure(background=background, foreground=foreground, activebackground=activebackground, activeforeground=activeforeground, disabledforeground=disabledforeground)
        self.border_frame.configure(highlightbackground=border_color)
