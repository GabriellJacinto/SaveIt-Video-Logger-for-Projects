import customtkinter
import tkinter as tk
from typing import List

from src.widgets import CreateGojectButton, ScrollableFrame, GojectEditFrame
from src.config import *

class GojectSelectWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, main_window, **kwargs):
        super().__init__(*args, **kwargs)
        self.__main_window = main_window
        self.projects_list = self.__main_window.settings_manager.projects
        self.goals_list = self.__main_window.settings_manager.goals
        self.title(GOJECT_SELECTION_WINDOW_NAME)
        self.geometry("{}x{}".format(GOJECT_SELECTION_WINDOW_WIDTH,GOJECT_SELECTION_WINDOW_HEIGHT))

    @property
    def main_window(self):
        return self.__main_window

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
    def __init__(self, *args, main_window, **kwargs):
        super().__init__(*args, **kwargs)
        self.__main_window = main_window
        self.__goals_widgets = []
        self.__projects_widgets = []

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
           
        self.create_button_1 = CreateGojectButton(master=self.tabview.tab("Add Goject"), toplevelwindow = self, width=GOJECT_EDIT_WINDOW_WIDTH)
        self.scrollable_frame_1 = ScrollableFrame(self.tabview.tab("Goals"), width=600)
        self.scrollable_frame_2 = ScrollableFrame(self.tabview.tab("Projects"), width=600)

        self.create_button_goals_tab = CreateGojectButton(master=self.tabview.tab("Goals"), toplevelwindow = self, width=GOJECT_EDIT_WINDOW_WIDTH)
        self.create_button_projects_tab = CreateGojectButton(master=self.tabview.tab("Projects"), toplevelwindow = self, width=GOJECT_EDIT_WINDOW_WIDTH)
        
        self.load_widgets()

    @property
    def main_window(self):
        return self.__main_window

    def load_widgets(self):
        self.create_button_1.show()

        self.projects_list = self.__main_window.settings_manager.projects
        self.goals_list = self.__main_window.settings_manager.goals

        if len(self.goals_list) == 0:
            self.create_button_goals_tab.show()
        else:
            self.scrollable_frame_1.grid(row=0, column=0, padx=(20, 10), pady=(10, 10))
            for i in range(len(self.goals_list)):
                goal_frame = GojectEditFrame(master=self.scrollable_frame_1.scrollable_canvas, toplevelwindow=self, row=i, 
                                            id=self.goals_list[i].id, name=self.goals_list[i].name, status=self.goals_list[i].status, 
                                            topic=self.goals_list[i].topic, due_date=self.goals_list[i].due_date)
                self.__goals_widgets.append(goal_frame)

        if len(self.projects_list) == 0:
            self.create_button_projects_tab.show()
        else:
            self.scrollable_frame_2.grid(row=0, column=0, padx=(20, 10), pady=(10, 10))
            for i in range(len(self.projects_list)):
                project_frame = GojectEditFrame(master=self.scrollable_frame_2.scrollable_canvas,toplevelwindow=self, row=i, 
                                                id=self.projects_list[i].id, name=self.projects_list[i].name, status=self.projects_list[i].status, 
                                                topic=self.projects_list[i].topic, due_date=self.projects_list[i].due_date)
                self.__projects_widgets.append(project_frame)

    def update_widgets_creation(self, type):
        if type == "Project":
            self.projects_list = self.__main_window.settings_manager.projects
            if self.create_button_projects_tab.visible:
                self.create_button_projects_tab.remove_all()
                self.scrollable_frame_2.grid(row=0, column=0, padx=(20, 10), pady=(10, 10))
            self.__projects_widgets = []
            for i in range(len(self.projects_list)):
                project_frame = GojectEditFrame(master=self.scrollable_frame_2.scrollable_canvas,toplevelwindow=self, row=i, 
                                                id=self.projects_list[i].id, name=self.projects_list[i].name, status=self.projects_list[i].status, 
                                                topic=self.projects_list[i].topic, due_date=self.projects_list[i].due_date)
                self.__projects_widgets.append(project_frame)
        elif type == "Goal":
            self.goals_list = self.__main_window.settings_manager.goals
            if self.create_button_goals_tab.visible:
                self.create_button_goals_tab.remove_all()
                self.scrollable_frame_1.grid(row=0, column=0, padx=(20, 10), pady=(10, 10))
            self.__goals_widgets = []
            for i in range(len(self.goals_list)):
                goal_frame = GojectEditFrame(master=self.scrollable_frame_1.scrollable_canvas, toplevelwindow=self, row=i, 
                                            id=self.goals_list[i].id, name=self.goals_list[i].name, status=self.goals_list[i].status, 
                                            topic=self.goals_list[i].topic, due_date=self.goals_list[i].due_date)
                self.__goals_widgets.append(goal_frame)
        else:
            print("Erro ao processar type '{}' no update de criação do widget".format(type))

    def update_widgets_deletion(self):
        self.projects_list = self.__main_window.settings_manager.projects
        self.goals_list = self.__main_window.settings_manager.goals
        
        if len(self.goals_list) == 0:
            self.scrollable_frame_1.grid_forget()
            self.create_button_goals_tab.show()
        else:
            self.scrollable_frame_1.grid(row=0, column=0, padx=(20, 10), pady=(10, 10))
            for goal_widget in self.__goals_widgets:
                goal_widget.remove_all()
            self.__goals_widgets = []
            for i in range(len(self.goals_list)):
                goal_frame = GojectEditFrame(master=self.scrollable_frame_1.scrollable_canvas, toplevelwindow=self, row=i, 
                                            id=self.goals_list[i].id, name=self.goals_list[i].name, status=self.goals_list[i].status, 
                                            topic=self.goals_list[i].topic, due_date=self.goals_list[i].due_date)
                self.__goals_widgets.append(goal_frame)

        if len(self.projects_list) == 0:
            self.scrollable_frame_2.grid_forget()
            self.create_button_projects_tab.show()
        else:
            self.scrollable_frame_2.grid(row=0, column=0, padx=(20, 10), pady=(10, 10))
            for project_widget in self.__projects_widgets:
                project_widget.remove_all()
            self.__projects_widgets = []
            for i in range(len(self.projects_list)):
                project_frame = GojectEditFrame(master=self.scrollable_frame_2.scrollable_canvas,toplevelwindow=self, row=i, 
                                                id=self.projects_list[i].id, name=self.projects_list[i].name, status=self.projects_list[i].status, 
                                                topic=self.projects_list[i].topic, due_date=self.projects_list[i].due_date)
                self.__projects_widgets.append(project_frame)

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