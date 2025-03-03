import tkinter as tk, sys

class ReadOnlyConsole(tk.Frame):
    def __init__(self, master):
        super().__init__(master, background="white")

        scr_bar = tk.Scrollbar(self, relief="flat")
        scr_bar.pack(side="right", fill="y")

        tk.Label(self, text="Read-Only Console", anchor="w").pack(fill='x')

        console = Console(self)
        console.pack(fill='x')
        
        console.config(yscrollcommand=scr_bar.set)
        scr_bar.config(command=console.yview)
        
class Console(tk.Text):
    def __init__(self, master, **options):
        super().__init__(master, **options)
        self.configure(state="disabled")
        
        self.pressed_enter= tk.BooleanVar(self, 0)
        self.input_value = ""

        self.bind("<Visibility>", self.set_stds)

    def set_stds(self, event):
        sys.stdout = event.widget
        sys.stderr = event.widget
        sys.stdin = event.widget
    
    def _readline(self, event):
        self.input_value= self.get(self.cursor_init_pos, "end")
        self.pressed_enter.set(1)
        
    def readline(self):
        self.focus()
        self.input_value = ""

        self.mark_set("insert", "end")
        self.cursor_init_pos = self.index("insert") 
        
        self.bind('<KeyRelease-Return>', self._readline)
        self.configure(state="normal")

        self.wait_variable(self.pressed_enter)

        self.pressed_enter.set(0)

        self.configure(state="disabled")
        return self.input_value

    def write(self, string):
        self.configure(state="normal")
        self.insert("end", string)
        self.configure(state="disabled")
    
    def destroy(self):
        # Modify variable to exit wait_var loop
        self.pressed_enter.set(0)
        self.pressed_enter.set(1)
        super().destroy()