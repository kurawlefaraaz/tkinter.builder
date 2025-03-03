from tkinter import Frame, Text, Listbox, Variable, Scrollbar
from tkinter.ttk import Style, Separator
class NumberedText(Frame):
    def __init__(self, master, **options):
        super().__init__(master, **options)

        self.config(bg='red')
        style = Style(self)
        self.configure(bg="white")
        style.configure("TSeparator", relief="flat")
        
        self.uniscrollbar = Scrollbar(self, relief="flat") # Scrollbar for listbox and text y-axis
        self.uniscrollbar.pack(side="right", fill="y")

        self.xscrollbar = Scrollbar(self, orient="horizontal",  relief="flat")
        self.xscrollbar.pack(side="bottom", fill="x")
        
        self.scroll_text()

        separator = Separator(self, orient='vertical')
        separator.pack(side="right", fill="y", padx=2)

        self.number_widget()
        
        self.textarea.config(spacing1=0, spacing2=0, spacing3=1)
        
    def scroll_text(self):
        self.textarea = Text(self, relief="flat", font="times 15", wrap="none", undo=1)

        self.uniscrollbar.config(command= self.scroll_both)
        self.xscrollbar.config(command=self.textarea.xview)
        self.textarea.config(xscrollcommand= self.xscrollbar.set, yscrollcommand = self.update_scroll_both)

        self.textarea.pack(side="right", fill="both", expand=1)
    
    def number_widget(self):
        self.linenumber = LineNumbers(self, self.textarea, relief="flat", state="disabled")

        self.uniscrollbar["command"] = self.scroll_both
        self.linenumber["yscrollcommand"] = self.update_scroll_both

        self.linenumber.pack(side="right", fill="y")
        
    def mouse_wheel(self, event):
        self.scrolltext.yview_scroll(int(-1*(event.delta/120)), "units")
        self.number_widget.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def scroll_both(self, action, position):
        self.textarea.yview_moveto(position)
        self.linenumber.yview_moveto(position)
    
    def update_scroll_both(self, first, last, type=None):
        self.textarea.yview_moveto(first)
        self.linenumber.yview_moveto(first)
        self.uniscrollbar.set(first, last)
    
    def get(self, index1, index2=None):
        return self.textarea.get(index1, index2)
    
    def delete(self, index1, index2=None):
        self.textarea.delete(index1, index2)

    def insert(self, index, chars, *args):
        self.textarea.insert(index, chars, *args)
        
class LineNumbers(Listbox):
    def __init__(self, master, textwidget, **options):
        super().__init__(master, **options)

        self.textwidget = textwidget

        self.textwidget.bind("<Return>", self.update_num_list)
        self.textwidget.bind("<KeyRelease-BackSpace>", self.update_num_list)
        self.textwidget.bind("<KeyRelease-Delete>", self.update_num_list)
        self.textwidget.bind("<<Modified>>", self.update_num_list)

        self.number_var = Variable(self, value=["1"])

        self.configure(listvariable=self.number_var, selectmode="single")
        self.set_width(1)
        self.set_font()

    def set_font(self):
        font = self.textwidget.cget("font")
        self.configure(font = font)

    def set_width(self, num_len):
        self.configure(width=num_len+1)

    def update_num_list(self, event):
        linenums = self.get_num_lines()

        number_list = list(range(1, linenums+1)) if event.keysym == "Return" else list(range(1, linenums))

        self.set_width(len(str(linenums)))
        self.number_var.set(number_list)
        self.yview("end")
        
    def get_num_lines(self):
        num_lines = int(self.textwidget.index("end").split(".")[0])
        return (num_lines)

    def get_current_colomn(self):
        curr_column = int(self.textwidget.index("insert").split(".")[1])
        return (curr_column)

    def get_current_row(self):
        curr_row = int(self.textwidget.index("insert").split(".")[0])
        return (curr_row)
