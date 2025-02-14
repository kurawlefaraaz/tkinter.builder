import tkinter as tk
import tkinter.ttk as ttk

# class FileMenu(tk.Menu):
#     def __init__(self, master, **options):
#         super().__init__(master, **options)

#         master.add_cascade(label ='File', menu = self)
#         self.add_command(
#             label='Exit',
#             command=master.destroy,
#         )

class ChooseTheme(tk.Menu):
    def __init__(self, master, **options):
        super().__init__(master, **options)

        master.add_cascade(label ='Choose Theme', menu = self)

        style = ttk.Style(self)
        for theme in style.theme_names():
            self.add_command(
                label=theme,
                command=lambda theme=theme: style.theme_use(theme),
            )

class GenerateCode(tk.Menu):
    def __init__(self, master, **options):
        super().__init__(master, **options)

        master.add_cascade(label ='Generate Code', menu = self)
        self.add_command(
            label='Generate Code',
            command=master.destroy,
        )
        # self.add_command(
        #     label='Generate Code for all frame',
        #     command=master.destroy,
        # )

class Help(tk.Menu):
    def __init__(self, master, **options):
        from webbrowser import open_new_tab
        super().__init__(master, **options)

        master.add_cascade(label ='Help', menu = self)
        self.add_command(
            label='About',
            command=master.destroy,
        )
        self.add_separator()
        self.add_command(
            label='Tkinter Builder Documentation',
            command=master.destroy,
        )

        tkinter_docs_menu = tk.Menu(self, tearoff=0)
        tkinter_docs_menu.add_command(
            label='Python Tkinter Documentation',
            command=lambda: open_new_tab("https://docs.python.org/3/library/tkinter.html"),
        )
        tkinter_docs_menu.add_command(
            label='Tcl Documentation',
            command=lambda: open_new_tab("https://tcl.tk/man/tcl8.6/TkCmd/contents.htm"),
        )
        self.add_cascade(label= "Tkinter Documentation", menu=tkinter_docs_menu)
        
class MenuBar(tk.Menu):
    # Located at top
    def __init__(self, master, **options):
        super().__init__(master, options)

        # self.file_menu = FileMenu(self, tearoff= 0)
        # self.add_separator()
        self.theme_menu = ChooseTheme(self, tearoff= 0)
        self.add_separator()
        self.generatecode_menu = GenerateCode(self, tearoff= 0)
        self.add_separator()
        self.help_menu = Help(self, tearoff= 0) 
        
        master.config(menu=self)

    