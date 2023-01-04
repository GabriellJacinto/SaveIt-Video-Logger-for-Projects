import customtkinter
import tkinter as tk
from typing import List

from src.widgets import CreateGojectButton, ScrollableFrame, GojectEditFrame
from src.config import *

class GojectSelectWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, main_window, record_type, **kwargs):
        super().__init__(*args, **kwargs)
        self.__main_window = main_window
        self.selected_gojects_id = []
        self.title(GOJECT_SELECTION_WINDOW_NAME)
        self.any_abled = False
        
        self.geometry("{}x{}".format(GOJECT_SELECTION_WINDOW_WIDTH,GOJECT_SELECTION_WINDOW_HEIGHT))
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)

        #Create Tab
        self.tabview = customtkinter.CTkTabview(self, width=550, height=600)
        self.tabview.grid(row=0, column = 0, columnspan=3, sticky="n")
        self.tabview.add("Goals")
        self.tabview.add("Projects")
        self.tabview.tab("Goals").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Projects").grid_columnconfigure(0, weight=1)

        self.scrollable_frame_1 = ScrollableFrame(self.tabview.tab("Goals"), width=500)
        self.scrollable_frame_2 = ScrollableFrame(self.tabview.tab("Projects"), width=500)
        self.empty_goals_message = customtkinter.CTkLabel(self.tabview.tab("Goals"), text="There are no available options. \n Please go to 'Gojects Configuration' to add new Goals", font = customtkinter.CTkFont(weight="bold"), text_color="red")
        self.empty_projects_message = customtkinter.CTkLabel(self.tabview.tab("Projects"), text="There are no available options. \n Please go to 'Gojects Configuration' to add new Projects", font = customtkinter.CTkFont(weight="bold"), text_color="red")

        self.record_button = customtkinter.CTkButton(self, border_width=2, text="Start Recording", command=lambda: self.start_recording(record_type), state="disabled", fg_color="transparent", text_color_disabled=("gray10", "#DCE4EE"))

        self.load_widgets()
          
    @property
    def main_window(self):
        return self.__main_window

    def load_widgets(self):
        self.record_button.grid(row=1, column = 1, pady = (10,10))

        self.projects_list = self.__main_window.settings_manager.projects
        self.goals_list = self.__main_window.settings_manager.goals

        if len(self.goals_list) == 0:
            self.empty_goals_message.grid()
        else:
            self.scrollable_frame_1.grid(row=0, column=0, padx=(20, 10), pady=(10, 10))
            for i in range(len(self.goals_list)):
                GojectEditFrame(master=self.scrollable_frame_1.scrollable_canvas, toplevelwindow=self, row=i, 
                                id=self.goals_list[i].id, name=self.goals_list[i].name, status=self.goals_list[i].status, 
                                topic=self.goals_list[i].topic, due_date=self.goals_list[i].due_date)
                
        if len(self.projects_list) == 0:
            self.empty_projects_message.grid()
        else:
            self.scrollable_frame_2.grid(row=0, column=0, padx=(20, 10), pady=(10, 10))
            for i in range(len(self.projects_list)):
                GojectEditFrame(master=self.scrollable_frame_2.scrollable_canvas,toplevelwindow=self, row=i, 
                                id=self.projects_list[i].id, name=self.projects_list[i].name, status=self.projects_list[i].status, 
                                topic=self.projects_list[i].topic, due_date=self.projects_list[i].due_date)

    def start_recording(self, record_type):
        self.withdraw()
        if record_type == "long_log":
            self.__main_window.start_long_log(self.selected_gojects_id)
        elif record_type == "quick_log":
            self.__main_window.start_quick_log(self.selected_gojects_id)
        else:
            print("Invalid recording type {}".format(record_type))

        
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
        self.tabview = customtkinter.CTkTabview(self, width=500, height=630)
        self.tabview.grid(row=0, column = 0, columnspan=3, sticky="n")
        self.tabview.add("Goals")
        self.tabview.add("Projects")
        self.tabview.add("Add Goject")
        self.tabview.tab("Goals").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Projects").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Add Goject").grid_columnconfigure(0, weight=1)
           
        self.create_button_1 = CreateGojectButton(master=self.tabview.tab("Add Goject"), toplevelwindow = self, width=GOJECT_EDIT_WINDOW_WIDTH)
        self.scrollable_frame_1 = ScrollableFrame(self.tabview.tab("Goals"), width=500)
        self.scrollable_frame_2 = ScrollableFrame(self.tabview.tab("Projects"), width=500)

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
                                            topic=self.goals_list[i].topic, due_date=self.goals_list[i].due_date, command="edit")
                self.__goals_widgets.append(goal_frame)

        if len(self.projects_list) == 0:
            self.create_button_projects_tab.show()
        else:
            self.scrollable_frame_2.grid(row=0, column=0, padx=(20, 10), pady=(10, 10))
            for i in range(len(self.projects_list)):
                project_frame = GojectEditFrame(master=self.scrollable_frame_2.scrollable_canvas,toplevelwindow=self, row=i, 
                                                id=self.projects_list[i].id, name=self.projects_list[i].name, status=self.projects_list[i].status, 
                                                topic=self.projects_list[i].topic, due_date=self.projects_list[i].due_date, command="edit")
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
                                                topic=self.projects_list[i].topic, due_date=self.projects_list[i].due_date, command="edit")
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
                                            topic=self.goals_list[i].topic, due_date=self.goals_list[i].due_date, command="edit")
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
                                            topic=self.goals_list[i].topic, due_date=self.goals_list[i].due_date, command="edit")
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
                                                topic=self.projects_list[i].topic, due_date=self.projects_list[i].due_date, command="edit")
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