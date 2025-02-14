import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import asksaveasfile as saveCodeFile, askopenfile as openCodeFile

from .dynamic_notebook import DynamicNotebook
from .frame_menubar import FrameMenubar
from .numbered_text import NumberedText

# TODO: Add save button to save the code to the widget specifically.
# TODO: Add save button to save the code to the program genearlized.
# TODO: Add load button to load code saved into the widget specifically.
# TODO: Use DynamicNotebook as parent

class ExecuteCodeFrame(tk.LabelFrame):
    def __init__(self, master, widget, **options) -> tk.LabelFrame:
        super().__init__(master, **options)

        self.widget= widget

        self.textbox = NumberedText(master=self)

        self.menu_bar()
        self.textbox.pack(padx=20, pady=5, fill="x")
    
    def menu_bar(self):
        menuFrame = FrameMenubar(self, relief= "flat")
        common_params = {"relief": "flat", "borderwidth": 0, "activebackground": "#A4D8E1", "padx": 10, "font": ("", "12")}

        menuFrame.setMenuButtonPackOptions(side="left")
        menuFrame.setMenuOptions(tearoff = 0)

        file_menu = menuFrame.addMenubutton(text="Files", **common_params)
        file_menu.add_command(label="Save", command=self.save_code)
        file_menu.add_command(label="Open", command=self.open_code)

        execute_code_menu = menuFrame.addMenubutton(text="Execute", **common_params)
        execute_code_menu.add_command(label="Execute", command=self.execute_code)

        menuFrame.pack(side="top", fill='x', padx=20)

    def execute_code(self):
        textarea_content = self.textbox.textarea.get(0.0, "end")
        print(vars(self.widget))
        print(self.widget._w)
        exec(textarea_content,{"ROOT": self.nametowidget("."), "WIDGET": self.widget}, vars(self.widget))

    def save_code(self):
        file_path = saveCodeFile()
        if file_path == None: return

        with file_path as file :
            textarea_content = self.textbox.textarea.get(0.0, "end")
            file.write(textarea_content)

    def open_code(self):
        file_path = openCodeFile()
        if file_path == None: return

        with file_path as file:
            content = file.read()
        self.textbox.textarea.delete(0.0, "end")
        self.textbox.textarea.insert(0.0, content)
        self.textbox.textarea.edit_modified(0)

class ExecuteCode(DynamicNotebook):
    def __init__(self, master, widget, **options):
        super().__init__(master)
        self.setDefualtFrame(ExecuteCodeFrame, master=self, widget=widget, **options)
        self.intialize_Frames()

def demo():
    root = tk.Tk()
    a=ExecuteCode(root)
    a.pack()
    root.mainloop()

if __name__ == "__main__":
    demo()