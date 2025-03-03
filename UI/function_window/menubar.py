import tkinter as tk
import tkinter.ttk as ttk
from tkinter.messagebox import showerror
from tkinter.filedialog import asksaveasfile

from widgets import ExecuteCodeFrame, BorderedButton
import utilities
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

        self.root = self.nametowidget(".")
        self.saved_code = {}
        self.scope = {}
        self.final_code = ""

        master.add_cascade(label ='Generate Code', menu = self)
        self.add_command(
            label='Generate Code',
            command=self.show_code,
        )

    def show_code(self):
        if (title:=self.root.method_window.title()) != "Widget Catalog":
            showerror("Instance Already Running", f"Instace of {title} Window is already running.", parent=self.root.method_window)
            return
        
        self.method_window_current_title = self.root.method_window.title()
        self.code_frame = ExecuteCodeFrame(self.nametowidget(".method_window"), self, height=400, width=600)
        self.code_frame.textbox.insert("1.0", self.get_final_code())
        self.root.method_window.title("Code")

        btn_frame = tk.Frame(self.code_frame)
        save_as_btn = BorderedButton(btn_frame, text="Save As", command=self.save_as_commnad, font="Courier 15 bold")
        save_as_btn.pack(side="left", padx=10, pady=10)

        cancel_btn = BorderedButton(btn_frame, text="Cancel", command=self.on_close, font="Courier 15 bold")
        cancel_btn.pack(side="left", padx=10, pady=10)
        btn_frame.pack()

        self.root.method_window.catalog.pack_forget()
        self.code_frame.pack(fill="both")
    
    def code_generation(self, master): 
        if not master: return

        for widget in self.root.widget_list.get_children(master):
            widget = self.nametowidget(widget)
            self.final_code += utilities.get_widget_code(widget)
            for val in widget.saved_code.values():
                self.final_code += val
            self.final_code += utilities.get_mgr_code(widget)
            self.code_generation(widget)


    def get_final_code(self):
        self.final_code += utilities.get_widget_code(self.root)
        for val in self.root.saved_code:
            self.final_code += val
        
        self.code_generation(self.root)

        self.final_code += "root.mainloop()"

        return self.final_code
    
    def save_as_commnad(self):
        if not (file:= asksaveasfile(parent=self.root.method_window)): return 
        file.write(self.code_frame.textbox.get("1.0", "end"))
        file.close()

    def on_close(self):
        self.final_code= ""

        self.root.method_window.title(self.method_window_current_title)
        self.code_frame.destroy()
        self.root.method_window.catalog.pack()


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
            label='tkinter.builder Documentation',
            command=master.destroy,
        )

        tkinter_docs_menu = tk.Menu(self, tearoff=0)
        tkinter_docs_menu.add_command(
            label='Python Tkinter Documentation',
            command=lambda: open_new_tab("https://docs.python.org/3/library/tkinter.html"),
        )
        tkinter_docs_menu.add_command(
            label="John Shipman's Tkinter Documentation",
            command=lambda: open_new_tab("https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/index.html"),
        )
        tkinter_docs_menu.add_command(
            label="TkDocs",
            command=lambda: open_new_tab("https://tkdocs.com/"),
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

    