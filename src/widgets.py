import customtkinter, tkinter
from typing import Union, Callable

import tkinter as tk
from tkinter import ttk


class ScrollableFrame(customtkinter.CTkFrame):
    def __init__(self, *args, width=200, height=650, **kwargs):
        super().__init__(*args, **kwargs)
        canvas = tk.Canvas(self,width = width, height = height, bd=0, highlightthickness=0, relief='ridge', bg='gray13')
        scrollbar = customtkinter.CTkScrollbar(self, orientation="vertical", command=canvas.yview)
        self.scrollable_canvas = customtkinter.CTkFrame(canvas)

        self.scrollable_canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=self.scrollable_canvas, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


class GojectSwitch(customtkinter.CTkFrame):
    def __init__(self, *args, width: int = 100, height: int = 32, command: Callable = None, **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)


class GojectCheckbox(customtkinter.CTkFrame):
    def __init__(self, *args, width: int = 100, height: int = 32, command: Callable = None, **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

    
class Spinbox(customtkinter.CTkFrame):
    def __init__(self, *args, width: int = 100, height: int = 32, step_size: Union[int, float] = 1, command: Callable = None, **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

        self.step_size = step_size
        self.command = command

        self.configure(fg_color=("gray78", "gray28"))  # set frame color

        self.grid_columnconfigure((0, 2), weight=0)  # buttons don't expand
        self.grid_columnconfigure(1, weight=1)  # entry expands

        self.subtract_button = customtkinter.CTkButton(self, text="-", width=height-6, height=height-6,
                                                       command=self.subtract_button_callback)
        self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3)

        self.entry = customtkinter.CTkEntry(self, width=width-(2*height), height=height-6, border_width=0)
        self.entry.grid(row=0, column=1, columnspan=1, padx=3, pady=3, sticky="ew")

        self.add_button = customtkinter.CTkButton(self, text="+", width=height-6, height=height-6,
                                                  command=self.add_button_callback)
        self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)

        # default value
        self.entry.insert(0, "0.0")

    def add_button_callback(self):
        if self.command is not None:
            self.command()
        try:
            value = float(self.entry.get()) + self.step_size
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
        except ValueError:
            return

    def subtract_button_callback(self):
        if self.command is not None:
            self.command()
        try:
            value = float(self.entry.get()) - self.step_size
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
        except ValueError:
            return

    def get(self) -> Union[float, None]:
        try:
            return float(self.entry.get())
        except ValueError:
            return None

    def set(self, value: float):
        self.entry.delete(0, "end")
        self.entry.insert(0, str(float(value)))