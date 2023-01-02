import customtkinter
import tkinter as tk
from typing import List

from src.widgets import CreateGojectButton
from src.config import *

class GojectSelectWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, main_window, data: List, **kwargs):
        super().__init__(*args, **kwargs)
        self.__main_window = main_window
        self.data = data
        self.title(GOJECT_SELECTION_WINDOW_NAME)
        self.geometry("{}x{}".format(GOJECT_SELECTION_WINDOW_WIDTH,GOJECT_SELECTION_WINDOW_HEIGHT))

    @property
    def parent(self):
        return self.__parent

        # create tabview
        """
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("CTkTabview")
        self.tabview.add("Tab 2")
        self.tabview.add("Tab 3")
        self.tabview.tab("CTkTabview").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Tab 2").grid_columnconfigure(0, weight=1)

        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("CTkTabview"), dynamic_resizing=False,
                                                        values=["Value 1", "Value 2", "Value Long Long Long"])
        self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.combobox_1 = customtkinter.CTkComboBox(self.tabview.tab("CTkTabview"),
                                                    values=["Value 1", "Value 2", "Value Long....."])
        self.combobox_1.grid(row=1, column=0, padx=20, pady=(10, 10))
        self.string_input_button = customtkinter.CTkButton(self.tabview.tab("CTkTabview"), text="Open CTkInputDialog",
                                                           command=self.open_input_dialog_event)
        self.string_input_button.grid(row=2, column=0, padx=20, pady=(10, 10))
        self.label_tab_2 = customtkinter.CTkLabel(self.tabview.tab("Tab 2"), text="CTkLabel on Tab 2")
        self.label_tab_2.grid(row=0, column=0, padx=20, pady=20)"""

"""
        self.select_gojects_label = ctk.CTkLabel(self.right_sidebar_frame, text="Selected Gojects", font=ctk.CTkFont(size=20, weight="bold"))
        self.select_gojects_label.grid(row=0, column=2, padx=20, pady=(20, 10))

        # create scrollable frame
        self.scrollable_frame = ScrollableFrame(self.right_sidebar_frame, width=RIGHT_FRAME_WIDTH)
        self.scrollable_frame.grid(row=1, column=2, padx=(20, 10), pady=(10, 10))

        for i in range(self.__settings_manager.goject_counter):
            goject_checkbox = GojectCheckbox(master=self.scrollable_frame.scrollable_canvas, name=self.__settings_manager.goject_buffer[i].name, status=self.__settings_manager.goject_buffer[i].status, type=self.__settings_manager.goject_buffer[i].type)
            selected_gojects_widgets.append(goject_checkbox)
        self.update()
"""

class GojectEditWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, main_window, data: List, **kwargs):
        super().__init__(*args, **kwargs)
        self.__main_window = main_window
        self.data = data

        self.title(GOJECT_EDIT_WINDOW_NAME)
        self.geometry("{}x{}".format(GOJECT_EDIT_WINDOW_WIDTH,GOJECT_EDIT_WINDOW_HEIGHT))
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)

        #Create Tab
        self.tabview = customtkinter.CTkTabview(self, width=600, height=630)
        self.tabview.grid(row=0, column = 0, columnspan=3, sticky="n")
        self.tabview.add("Goals")
        self.tabview.add("Projects")
        self.tabview.add("Add Goject")
        self.tabview.tab("Goals").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Projects").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Add Goject").grid_columnconfigure(0, weight=1)
        
        #Create Bottom Frame   
        self.create_button = CreateGojectButton(master=self.tabview.tab("Add Goject"), toplevelwindow = self, width=GOJECT_EDIT_WINDOW_WIDTH)

        self.test = customtkinter.CTkFrame(self.tabview.tab("Goals"))
        self.test.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.test, dynamic_resizing=False,
                                                        values=["Value 1", "Value 2", "Value Long Long Long"])
        self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.combobox_1 = customtkinter.CTkComboBox(self.tabview.tab("Goals"),
                                                    values=["Value 1", "Value 2", "Value Long....."])
        self.combobox_1.grid(row=1, column=0, padx=20, pady=(10, 10))
        self.string_input_button = customtkinter.CTkButton(self.tabview.tab("Goals"), text="Open CTkInputDialog",
                                                           command=self.open_input_dialog_event)
        self.string_input_button.grid(row=2, column=0, padx=20, pady=(10, 10))
        self.label_tab_2 = customtkinter.CTkLabel(self.tabview.tab("Projects"), text="CTkLabel on Tab 2")
        self.label_tab_2.grid(row=0, column=0, padx=20, pady=20)        

    @property
    def main_window(self):
        return self.__main_window

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

# create tabview
"""
        self.select_gojects_label = ctk.CTkLabel(self.right_sidebar_frame, text="Selected Gojects", font=ctk.CTkFont(size=20, weight="bold"))
        self.select_gojects_label.grid(row=0, column=2, padx=20, pady=(20, 10))

        # create scrollable frame
        self.scrollable_frame = ScrollableFrame(self.right_sidebar_frame, width=RIGHT_FRAME_WIDTH)
        self.scrollable_frame.grid(row=1, column=2, padx=(20, 10), pady=(10, 10))

        for i in range(self.__settings_manager.goject_counter):
            goject_checkbox = GojectCheckbox(master=self.scrollable_frame.scrollable_canvas, name=self.__settings_manager.goject_buffer[i].name, status=self.__settings_manager.goject_buffer[i].status, type=self.__settings_manager.goject_buffer[i].type)
            selected_gojects_widgets.append(goject_checkbox)
        self.update()
"""

class ProcessDataWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, main_window, data, **kwargs):
        super().__init__(*args, **kwargs)
        self.__main_window = main_window
        self.title(GOJECT_EDIT_WINDOW_NAME)
        self.geometry("{}x{}".format(GOJECT_EDIT_WINDOW_WIDTH,GOJECT_EDIT_WINDOW_HEIGHT))

    @property
    def main_window(self):
        return self.__main_window

if __name__ == '__main__':
    customtkinter.set_appearance_mode(APP_COLOR_THEME)
    customtkinter.set_default_color_theme(APP_WIDGETS_COLORS)
    class Application(customtkinter.CTk):
        def __init__(self):
            super().__init__()
        
        def draw(self):
            #GojectSelectWindow(parent="hello", data = "hi")
            GojectEditWindow(parent="hello", data = "hi")
            #ProcessDataWindow(parent="hello", data = "hi")

        def __call__(self):
            self.draw()
            self.mainloop()

    app = Application()
    app()