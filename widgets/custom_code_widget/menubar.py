from tkinter import StringVar, OptionMenu
from tkinter.filedialog import asksaveasfile as saveCodeFile, askopenfile as openCodeFile
from tkinter.messagebox import showinfo

import tkinter as tk
import tkinter.ttk as ttk

from widgets import PlaceholderedEntry
from utilities import create_widget

from .frame_menubar import FrameMenubar

class Menubar(FrameMenubar):
    def __init__(self, master, widget):
        super().__init__(master, relief= "flat")

        self.root = self.nametowidget(".")
        self.widget = widget
        self.parems = {"relief": "flat", "borderwidth": 0, "activebackground": "#A4D8E1", "padx": 10, "font": ("", "12")}

        self.setMenuButtonPackOptions(side="left")
        self.setMenuOptions(tearoff=0)

        self.file_menu()
        self.execute_code_menu()

        self.pack(side="top", fill='x', padx=20, expand=1)
    
    def file_menu(self):
        self.file_menu = self.addMenubutton(text="Files", **self.parems)
        self.file_menu.add_command(label="Save", command=self.save_command)
        self.file_menu.add_command(label="Save As", command=self.save_as_command)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Load", command=self.load_command)
        self.file_menu.add_command(label="Load File", command=self.load_file_command)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Reset Execution scope", command=self.reset_exec_scope)
    
    def execute_code_menu(self):
        execute_code_menu = self.addMenubutton(text="Execute", **self.parems)
        execute_code_menu.add_command(label="Execute", command=self.execute_command)

    def notebook_menu(self):
        notebook_m = self.addMenubutton(text="Notebook", **self.parems)
        notebook_m.add_command(label="New Tab", command=self.master.master.add_frame)
    
    def save_command(self):
        textarea_content = self.master.textbox.get(0.0, "end")

        code_name_entry= PlaceholderedEntry(self, placeholder="Code Name:")
        var = StringVar(code_name_entry, "Code Name: ")
        code_name_entry["textvariable"] =  var

        code_name_entry.bind("<Return>", lambda e: code_name_entry.destroy())
        code_name_entry.bind("<FocusOut>", lambda e: code_name_entry.destroy())
        code_name_entry.pack(side="left")
        code_name_entry.wait_window()
        
        code_name = var.get()
        if not code_name: return
        self.widget.saved_code.update({code_name: textarea_content})
        showinfo("Success", f"Code is saved as {code_name}", parent=self)
    
    def save_as_command(self):
        file_path = saveCodeFile()
        if file_path == None: return

        with file_path as file :
            textarea_content = self.textbox.textarea.get(0.0, "end")
            file.write(textarea_content)

    def load_command(self):
        options = list(self.widget.saved_code.keys()) 
        if not options: return

        var = StringVar(self, options[0])

        def insert_code(value):
            self.master.textbox.insert("current", self.widget.saved_code.get(value))
            self.master.textbox.textarea.edit_modified(0)
            options_menu.destroy()

        options_menu = OptionMenu(self, var, *options, command=insert_code)
        options_menu.bind("<Return>", lambda e: options_menu.destroy())
        options_menu.bind("<FocusOut>", lambda e: options_menu.destroy())
        options_menu.pack(side="left")

    def load_file_command(self):
        file_path = openCodeFile()
        if file_path == None: return

        with file_path as file:
            content = file.read()
            
        self.master.textbox.delete(0.0, "end")
        self.master.textbox.insert(0.0, content)
        self.master.textbox.textarea.edit_modified(0)

    def execute_command(self):
        textarea_content = self.master.textbox.get(0.0, "end")
        exec(textarea_content,{"ROOT": self.root, "WIDGET": self.widget, "tk": tk, "ttk": ttk}, self.widget.scope)
        self.nametowidget('.').widget_list.refresh_widget_list()
        showinfo("Success", "Code is successfully executed", parent=self)
    
    def reset_exec_scope(self):
        self.widget.scope = {}
        showinfo("Success", "Execution Scope is reseted.", parent=self)



