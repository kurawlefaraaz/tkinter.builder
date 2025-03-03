import tkinter as tk
from tkinter.messagebox import askretrycancel
from widgets import BorderedButton, PlaceholderedEntry

class SetupEntry(PlaceholderedEntry):
    def __init__(self, master=None, placeholder="", name= None):
        super().__init__(master, placeholder, name= name, background= "white", borderwidth= "25", font= "Courier 15", foreground= "black", highlightbackground= "#5185b4", highlightthickness= "3", relief= "flat")
        self.indicate_normal()

    def indicate_error(self, error_text, timeout=500):
        self.configure(highlightcolor="red", highlightbackground="red")

        error_label = tk.Label(self, text=error_text, background="white", font="Courier 15", foreground="SystemWindowText", anchor="w", padx=0, pady=0)
        error_label.pack(fill="x")
        error_label.after(timeout, error_label.destroy)

        self.after(timeout, self.indicate_normal)
    
    def indicate_normal(self):
        self.configure(highlightcolor="green", highlightbackground="#5185b4")

class GetWidgetSetupData(tk.Frame):
    def __init__(self, master, **options):
        super().__init__(master, bg="white", highlightbackground="black", highlightthickness=2, **options)
        self.pack(expand=1, padx=30, pady=(0, 30), fill="both")
        self.output = None

        self.add_titles()
        self.add_entries()
        self.add_submit_cancel_button()
        self.add_note()

        self.wait_window()
        
    def add_titles(self):
        titles_frame = tk.Frame(self, name= "title_frame", background= "white")

        title = tk.Label(titles_frame, name= "title", background= "white", font= "terminal 30", foreground= "black", text= "Enter Details")
        title.pack(anchor= "n", fill= "x", padx=0, pady=0)

        sub_title = tk.Label(titles_frame, name= "sub_title", background= "white", font= "terminal 12", foreground= "black", text= "for widget setup")
        sub_title.pack(anchor= "n", fill="x", padx=0, pady=0)

        titles_frame.pack(anchor='n', padx=20, pady=30)
    
    def add_entries(self):
        entries_frame = tk.Frame(self, name= "entries_frame", background= "white")

        self.widget_master_entry = SetupEntry(entries_frame, placeholder= "*Master: ", name= "widget_master_entry")
        self.widget_master_entry.pack(fill= "x", padx= 20, pady= 20)

        self.widget_name_entry = SetupEntry(entries_frame, placeholder= "Name: ", name= "widget_name_entry")
        self.widget_name_entry.pack(fill= "x", padx= 20, pady= 20)

        entries_frame.pack(fill= 'x')
    
    def add_submit_cancel_button(self):
        buttons_frame= tk.Frame(self, background = "white")

        submit_btn = BorderedButton(buttons_frame, text= "Submit", font= "TkDefaultFont 15 bold", command= self.on_submit)
        submit_btn.set_colors(background= "#524d4d", foreground= "white")
        submit_btn.pack(side= "left", padx=20)

        cancel_btn =BorderedButton(buttons_frame, text= "Cancel", font= "TkDefaultFont 15 bold", command= self.destroy)
        cancel_btn.set_colors(background= "#524d4d", foreground= "white")
        cancel_btn.pack(side= "left", padx=20)

        buttons_frame.pack(padx=20, pady=20)
    
    def add_note(self):
        note = tk.Label(self, text= "* indicates mandatory field", background="white", foreground="grey")
        note.pack(side="bottom", anchor='sw', padx=20)
    
    def on_submit(self):
        master_text = self.widget_master_entry.get().replace("*Master: ", "")
        name_text = self.widget_name_entry.get().replace("Name: ", "")

        self.nametowidget(".").nametowidget(master_text) # Validating master
        is_0_index_digit = name_text[0].isdigit() if len(name_text) else 0
        if name_text.find(" ") != -1 or name_text.find(".") != -1 or is_0_index_digit:
            raise tk.TclError(f"Invalid Name: {name_text}")
        
        retry = 0
        if not master_text :
            self.widget_master_entry.indicate_error("Master Required!")
            return

        if retry:
            return
        else:
            self.output = {"master": self.nametowidget(master_text), "name": name_text}
            self.destroy()
            
    def get(self):
         return self.output

def demo():
    root = tk.Tk()
    root.configure(bg="white")
    a= GetWidgetSetupData(root)
    print(a.get())
    root.mainloop()

if __name__ == "__main__":
    demo()