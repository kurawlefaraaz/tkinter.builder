import tkinter as tk
import tkinter.ttk as ttk
from tkinter.font import Font

from UI import Creation_UI
from widgets import ExecuteCode, BorderedButton

from .widget_list import WidgetList

tk_widget_dict = {
        "Button": tk.Button,
        "Frame": tk.Frame,
        "Label": tk.Label,
        "Entry": tk.Entry,
        "Listbox": tk.Listbox,
        "Menubutton": tk.Menubutton,
        "Radiobutton": tk.Radiobutton,
        "Text": tk.Text,
        "Checkbutton": tk.Checkbutton,
        "Menu": tk.Menu,
        "LabelFrame": tk.LabelFrame,
        "PanedWindow": tk.PanedWindow,
        "SpinBox": tk.Spinbox,
        "Scrollbar": tk.Scrollbar,
        "Scale": tk.Scale,
        "Message": tk.Message,
        "Canvas": tk.Canvas
        }

ttk_widget_dict = {
        "Button": ttk.Button,
        "Frame": ttk.Frame,
        "Label": ttk.Label,
        "Entry": ttk.Entry,
        "Menubutton": ttk.Menubutton,
        "Radiobutton": ttk.Radiobutton,
        "LabelFrame": ttk.LabelFrame,
        "PanedWindow": ttk.PanedWindow,
        "SpinBox": ttk.Spinbox,
        "Scrollbar": ttk.Scrollbar,
        "Scrollbar": ttk.Scrollbar,
        "Checkbutton": ttk.Checkbutton,
        "ComboBox": ttk.Combobox,
        "NoteBook": ttk.Notebook,
        "ProgressBar": ttk.Progressbar,
        "Separator": ttk.Separator,
        "Sizegrip": ttk.Sizegrip,
        "TreeView": ttk.Treeview,
    }

class DropFrame(BorderedButton):
    def __init__(self, master,frame, on_hide_func, on_show_func, font, text, symbol=("▼", "▲"), name= None):
        self.frame_invisible_text ,self.frame_visible_text = f"{text} {symbol[0]}", f"{text} {symbol[1]}"
        self.frame = frame
        self.text = text
        self.counter = 0
        self.on_hide_func = on_hide_func
        self.on_show_func = on_show_func

        super().__init__(master, name=name, text = self.frame_invisible_text, command=self.toggle, font=font)
    
    def _show_frame(self): 
        self.counter = 1
        self.frame.pack(fill="both")
        self.on_show_func()
        self.configure(text= self.frame_visible_text)

    def _hide_frame(self):
        self.counter = 0
        self.frame.pack_forget()
        self.on_hide_func()
        self.configure(text= self.frame_invisible_text)
    
    def toggle(self):
        if self.counter: self._hide_frame()
        else: self._show_frame()

class WidgetCatalog(tk.Frame):
    def __init__(self, master):
        super().__init__(master, name="widget_catalog", background="white", padx=10, pady=10)

        self.master.title("Widget Catalog")

        btn_frame = tk.Frame(self, background="white")

        catalog_title_btn_font = Font(self, family="TkDefaultFont", weight="bold", size= 15)

        self.tk_widget_btn= DropFrame(btn_frame, self.tk_catalog_frame(), self._enable_drop_frames, self._disable_drop_frames, text="Tk Widgets", font=catalog_title_btn_font, name="tk_button")
        self.tk_widget_btn.grid(row=0, column=0, padx=10, pady=5)

        self.ttk_widget_btn= DropFrame(btn_frame, self.ttk_catalog_frame(), self._enable_drop_frames, self._disable_drop_frames, text="Ttk Widgets", font=catalog_title_btn_font, name="ttk_button")
        self.ttk_widget_btn.grid(row=0, column=1, padx=10, pady=5)

        self.execute_code_widget_btn= DropFrame(btn_frame, self.execute_code_catalog_frame(), self._enable_drop_frames, self._disable_drop_frames, text="Execute Code", font=catalog_title_btn_font, name="execute_button")
        self.execute_code_widget_btn.grid(row=1, column=0, padx=10, pady=5)

        self.widget_list_btn= DropFrame(btn_frame, self.widget_list_frame(), self._enable_drop_frames, self._disable_drop_frames, text="Widget List", font=catalog_title_btn_font, name="tk_button")
        self.widget_list_btn.grid(row=1, column=1, padx=10, pady=5)

        btn_frame.pack()

        self.pack()

    def tk_catalog_frame(self):
        TK_Catalog_Frame = tk.Frame(self, name="tk_frame", bg='white', padx=10, pady=10)
        self._GridWidget_catalog(TK_Catalog_Frame, tk_widget_dict)
        return TK_Catalog_Frame
    
    def ttk_catalog_frame(self):
        TtK_Catalog_Frame = tk.Frame(
            self, name="ttk_frame", bg='white', padx=10, pady=10
        )
        self._GridWidget_catalog(TtK_Catalog_Frame, ttk_widget_dict)
        return TtK_Catalog_Frame

    def execute_code_catalog_frame(self):
        frame = tk.Frame(self, name="execute_code_frame", background="white", padx=10, pady=10)
        custom_code = ExecuteCode(frame, self.master.master)
        custom_code.pack()
        return frame

    def widget_list_frame(self):
        frame = tk.Frame(self, name="widget_list_frame", background="white", padx=10, pady=10)
        top = tk.Frame(frame, background="white")
        wl = WidgetList(frame)
        tk.Label(top, text="Double click on the widget row to get Update UI", background="white").pack(side="left",anchor='w')
        tk.Button(top, text="Refresh", background="white", command=wl.refresh_widget_list).pack(side="right",anchor='w')
        top.pack(fill="x")
        wl.pack(fill="both")

        return frame
    
    def _GridWidget_catalog(self, FrameName, widget_dict):  # Creates Buttons for each widget in widget_dict.
        catalog_list_btn_font = Font(self, family="TkDefaultFont", weight="normal")
        row, column = 0, 0
        for key, value in widget_dict.items():
            if column == 5:
                row += 1
                column = 0

            btn = BorderedButton(
                FrameName,
                text=key,
                command=lambda widget_class=value: self.on_widget_button_press(widget_class=widget_class),
                font=catalog_list_btn_font
            )
            btn.set_colors(foreground="#5185b4")
            btn.grid(row=row, column=column, padx=5, pady=5)

            column += 1
    
    def _disable_drop_frames(self):
        for widget in (self.tk_widget_btn, self.ttk_widget_btn, self.execute_code_widget_btn, self.widget_list_btn):
            if not widget.counter:
                widget.configure(state="disabled")
    
    def _enable_drop_frames(self):
        for widget in (self.tk_widget_btn, self.ttk_widget_btn, self.execute_code_widget_btn, self.widget_list_btn):
            widget.configure(state="normal")
    
    def reinvoke_enable_button(self):
        for widget in (self.tk_widget_btn, self.ttk_widget_btn, self.execute_code_widget_btn, self.widget_list_btn):
            
            if "▲" in widget.cget("text"): 
                widget.invoke()
                return
            
    def on_widget_button_press(self, widget_class):
        creation_window = Creation_UI(self.master, widget_class=widget_class)
    
def demo():
    root = tk.Tk()
    root.resizable(0, 0)
    A = WidgetCatalog(root)
    root.mainloop()
    
if __name__ == "__main__":
    demo()
