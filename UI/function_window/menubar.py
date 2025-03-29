import tkinter as tk
import tkinter.ttk as ttk
from tkinter.messagebox import showerror
from tkinter.filedialog import asksaveasfile
from webbrowser import open_new_tab

from widgets import ExecuteCodeFrame, BorderedButton
import utilities

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
        self.window = tk.Toplevel(self.master)
        self.window.grab_set()

        self.code_frame = ExecuteCodeFrame(self.window, self, height=400, width=600)
        self.code_frame.textbox.insert("1.0", self.get_final_code())

        btn_frame = tk.Frame(self.code_frame)
        save_as_btn = BorderedButton(btn_frame, text="Save As", command=self.save_as_commnad, font="Courier 15 bold")
        save_as_btn.pack(side="left", padx=10, pady=10)

        cancel_btn = BorderedButton(btn_frame, text="Cancel", command=self.on_close, font="Courier 15 bold")
        cancel_btn.pack(side="left", padx=10, pady=10)
        btn_frame.pack()

        self.code_frame.pack(fill="both")
    
    def code_generation(self, master): 
        if not master: return

        for widget in self.root.widget_list.get_children(master):
            widget = self.nametowidget(widget)
            self.final_code += utilities.get_widget_code(widget)
            for val in widget.saved_code.values():
                val=val.replace("WIDGET", widget.winfo_name())
                self.final_code += val
            self.final_code += utilities.get_mgr_code(widget)
            self.code_generation(widget)


    def get_final_code(self):
        if self.root.nametowidget(".method_window").title() != "Widget Catalog": wid = self.root.last_touched_widget
        else: 
            wid=self.root
        self.final_code += utilities.get_widget_code(wid)
        for val in wid.saved_code.values():
            val=val.replace("WIDGET", "root")
            self.final_code += val
        
        self.code_generation(wid)
        self.final_code += "" if not utilities.get_mgr_code(wid) else utilities.get_mgr_code(wid) 
        if self.root.nametowidget(".method_window").title() == "Widget Catalog":self.final_code += "root.mainloop()"

        return self.final_code
    
    def save_as_commnad(self):
        if not (file:= asksaveasfile(parent=self.root.method_window)): return 
        file.write(self.code_frame.textbox.get("1.0", "end"))
        file.close()

    def on_close(self):
        self.final_code= ""
        self.window.destroy()


class Help(tk.Menu):
    def __init__(self, master, **options):
        super().__init__(master, **options)

        master.add_cascade(label ='Help', menu = self)
        self.add_command(
            label='About',
            command=About,
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

        self.theme_menu = ChooseTheme(self, tearoff= 0)
        self.add_separator()
        self.generatecode_menu = GenerateCode(self, tearoff= 0)
        self.add_separator()
        self.help_menu = Help(self, tearoff= 0) 
        
        master.config(menu=self)


class About(tk.Toplevel):
    def __init__(self):
        super().__init__( background="white")
        self.geometry("500x250")

        title = tk.Label(self, name= "title", text= "tkinter.builder", font= "TkHeadingFont 24 bold roman", background= "white")
        title.pack()

        group_vers = tk.Frame(self, background="white")
        app_ver = tk.Label(group_vers, name= "app_ver", anchor= "w", background= "white", text= "App version: 1.0")
        app_ver.pack(padx= "10", side="left")
        py_ver = tk.Label(group_vers, name= "py_ver", text= "Python version: 3.x", anchor= "w", background= "white")
        py_ver.pack(padx= "10", side="left")
        tk_ver = tk.Label(group_vers, name= "tk_ver", background= "white", text= "Tk version: 8.x", anchor= "w")
        tk_ver.pack(padx= "10", side="left")
        group_vers.pack()

        about_text= """RAD tool developed by Faraaz Kurawle, to speedify GUI developement in 
        tkinter with python. """ 
        about = tk.Label(self, name= "about", background= "white", text=about_text)
        about.pack(pady=(40,20))

        group_links = tk.Frame(self, background="white")
        github = tk.Label(group_links, name= "github", anchor= "w", background= "white", text= "Github Source", foreground="blue", font="TkDefault 10 underline", cursor="hand1")
        github.bind("<Button-1>", lambda e: open_new_tab("https://github.com/kurawlefaraaz/tkinter.builder"))
        github.pack(fill='x', padx= "10", side="left")
        license = tk.Label(group_links, name= "licence", text= "See Licence", anchor= "w", background= "white", foreground="blue", font="TkDefault 10 underline", cursor="hand1")
        license.bind("<Button-1>", lambda e: open_new_tab("https://mit-license.org/"))
        license.pack(fill='x', padx= "10", side="right")
        group_links.pack(fill='x', padx=30, side="bottom")
