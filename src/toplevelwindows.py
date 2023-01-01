import customtkinter
import tkinter as tk

from src.config import *

class GojectSelectWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, parent, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent
        self.title(GOJECT_SELECTION_WINDOW_NAME)
        self.geometry("{}x{}".format(GOJECT_SELECTION_WINDOW_WIDTH,GOJECT_SELECTION_WINDOW_HEIGHT))


class GojectEditWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, parent, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent
        self.title(GOJECT_EDIT_WINDOW_NAME)
        self.geometry("{}x{}".format(GOJECT_EDIT_WINDOW_WIDTH,GOJECT_EDIT_WINDOW_HEIGHT))


class ProcessDataWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, parent, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent
        self.title(GOJECT_EDIT_WINDOW_NAME)
        self.geometry("{}x{}".format(GOJECT_EDIT_WINDOW_WIDTH,GOJECT_EDIT_WINDOW_HEIGHT))