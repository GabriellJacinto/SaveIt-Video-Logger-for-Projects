import customtkinter
import tkinter as tk
from typing import Union, Callable

from src.config import COLORS, TOPICS, MAIN_WINDOW_NAME

class CreateGojectButton(customtkinter.CTkFrame):
    def __init__(self, *args, master, toplevelwindow, width=200, **kwargs):
        super().__init__(*args, master=master, **kwargs)
        self.toplevelwindow = toplevelwindow
        self.visible = False

        self.bottom_frame = customtkinter.CTkFrame(master, width=width)
        
        self.create_button = customtkinter.CTkButton(master=self.bottom_frame, text="New Goject", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.create_button_press)
    
        self.name_entry = customtkinter.CTkEntry(self.bottom_frame, placeholder_text="Name")
        self.status_option = customtkinter.CTkOptionMenu(self.bottom_frame, dynamic_resizing=False, values=["Backlog", "In Progress", "Completed"])
        self.type_option = customtkinter.CTkOptionMenu(self.bottom_frame, dynamic_resizing=False,values=["Goal", "Project"])
        self.date_entry = customtkinter.CTkEntry(self.bottom_frame, placeholder_text="Due Date (D/M/YYYY)")
        self.topics_option = customtkinter.CTkComboBox(self.bottom_frame, values=list(TOPICS.keys()))
        self.save_button = customtkinter.CTkButton(master=self.bottom_frame, border_width=2, text="Save", command=self.save_button_press, fg_color="green")

        self.topics_option.set("Topic")
        self.status_option.set("Status")
        self.type_option.set("Type")    

    def show(self):
        self.bottom_frame.grid(row=0, column=0, columnspan = 2, pady=(5, 0))
        self.bottom_frame.grid_columnconfigure(0,weight=0)
        self.bottom_frame.grid_columnconfigure((1,2),weight=0)
        self.bottom_frame.grid_rowconfigure((0, 1, 2, 3), weight=0)
        self.create_button.grid(row=0, column=1, padx=(5, 5), pady=(5, 5), sticky="nswe")
        self.visible = True

    def remove_all(self):
        self.bottom_frame.grid_forget()
        self.create_button.grid_forget()
        self.name_entry.grid_forget()
        self.topics_option.grid_forget()
        self.date_entry.grid_forget()
        self.status_option.grid_forget()
        self.save_button.grid_forget()
        self.visible = False

    def create_button_press(self):
        self.name_entry.grid(row=1, column=0, columnspan=3, padx=(5, 5), pady=(5, 5), sticky="nsew")
        self.topics_option.grid(row=3, column=1, padx=(5, 5), pady=(5, 5))
        self.date_entry.grid(row=3, column=0, padx=(5, 5), pady=(5, 5))
        self.type_option.grid(row=2, column=1, padx=(5, 5), pady=(5, 5))
        self.status_option.grid(row=2, column=0, padx=(5, 5), pady=(5, 5))
        self.save_button.grid(row=3, column=2, sticky="nsew", padx=(5, 5), pady=(5, 5))
    
    def save_button_press(self):
        name = self.name_entry.get()
        type = self.type_option.get()
        status = self.status_option.get()
        topic = self.topics_option.get()
        due_date = self.date_entry.get()

        self.toplevelwindow.main_window.settings_manager.create_goject(name, type, status, topic, due_date)
        self.toplevelwindow.update_widgets_creation(type)
        
        self.name_entry.delete(0,len(name))
        self.date_entry.delete(0,len(due_date))
        self.topics_option.set("Topic")
        self.status_option.set("Status")
        self.type_option.set("Type")

class ScrollableFrame(customtkinter.CTkFrame):
    def __init__(self, *args, width=200, height=650, **kwargs):
        super().__init__(*args, **kwargs)
        canvas = tk.Canvas(self,width = width, height = height, bd=0, highlightthickness=0, relief='ridge', bg='gray13')
        scrollbar = customtkinter.CTkScrollbar(self, orientation="vertical", command=canvas.yview)
        self.scrollable_canvas = customtkinter.CTkFrame(canvas)

        self.scrollable_canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=self.scrollable_canvas, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        #canvas.pack(side="left", fill="both", expand=True)
        #scrollbar.pack(side="right", fill="y")

        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

class GojectEditFrame(customtkinter.CTkFrame):
    def __init__(self, *args, master, toplevelwindow, row, id, name: str = "Example", status: str = "Backlog", topic: str = "", due_date: str = "", width: int = 200, height: int = 32, foreground_color="transparent", **kwargs):
        super().__init__(*args, master=master, width=width, height=height, fg_color=foreground_color, **kwargs)
        self.toplevelwindow = toplevelwindow
        self.id = id
        self.name = name
        self.status = status
        self.topic = topic
        
        self.grid(row=row, column=0, padx=(10, 10), pady=(5, 10), sticky="w")
        self.grid_columnconfigure(0,weight=1)
        self.grid_columnconfigure(1,weight=0)
        self.grid_rowconfigure((0, 1, 2, 3), weight=0)
        
        self.switch = customtkinter.CTkSwitch(self, text="{} ({})".format(self.name, status), font = customtkinter.CTkFont(weight="bold"), text_color=COLORS[status],command=self.switch_select)
        self.topic_date_label = customtkinter.CTkLabel(self, text="{} \t {}".format(topic, due_date), font = customtkinter.CTkFont(size = 10))        
        self.edit_name_button = customtkinter.CTkButton(self, border_width=2, text="Rename", command=self.edit_name_button_press)
        self.status_option = customtkinter.CTkOptionMenu(self, dynamic_resizing=False, values=["Backlog", "In Progress", "Completed"], command=self.edit_status_button_press)
        self.edit_date_button = customtkinter.CTkButton(self, border_width=2, text="Due Date", command=self.edit_date_button_press)
        self.delete_button = customtkinter.CTkButton(self, border_width=2, text="Delete", command=self.delete_button_press, fg_color="red")

        self.switch.grid(row=0, column=0, columnspan=4, pady=(5, 0), padx=(5, 5), sticky="w")   
        self.topic_date_label.grid(row=1, column=0, columnspan=4, pady=(5, 0),padx=(5, 5), sticky="w") 

    def remove_all(self):
        self.grid_forget()
        self.switch.grid_forget()
        self.topic_date_label.grid_forget()
        self.edit_name_button.grid_forget()
        self.status_option.grid_forget()
        self.edit_date_button.grid_forget()
        self.delete_button.grid_forget()

    def switch_select(self):
        value = self.switch.get()
        if(value):
            self.edit_name_button.grid(row=2, column=0, pady=(5, 0))
            self.status_option.grid(row=2, column=1, pady=(5, 0))
            self.edit_date_button.grid(row=3, column=0, pady=(5, 0))
            self.delete_button.grid(row=3, column=1, pady=(5, 0))
        else:
            self.edit_name_button.grid_forget()
            self.status_option.grid_forget()
            self.edit_date_button.grid_forget()
            self.delete_button.grid_forget()

    def edit_date_button_press(self):
        dialog = customtkinter.CTkInputDialog(text="Type a new Due Date (D/M/YYYY):", title="{} - Edit Due Date".format(MAIN_WINDOW_NAME))
        value = dialog.get_input()
        if value == "":
            print("Valor Invalido")
        else:
            self.toplevelwindow.main_window.settings_manager.alter_goject(self.id, "due_date", value)
            self.topic_date_label.configure(text="{} \t {}".format(self.topic, value))

    def edit_status_button_press(self, new_status):
        self.toplevelwindow.main_window.settings_manager.alter_goject(self.id, "status", new_status)
        self.switch.configure(text="{} ({})".format(self.name, new_status), text_color=COLORS[new_status])
    
    def edit_name_button_press(self):
        dialog = customtkinter.CTkInputDialog(text="Type a new Name:", title="{} - Edit Name".format(MAIN_WINDOW_NAME))
        value = dialog.get_input()
        if value == "" or value == None:
            print("Valor Invalido")
        else:
            self.toplevelwindow.main_window.settings_manager.alter_goject(self.id, "name", value)
            self.switch.configure(text="{} ({})".format(value, self.status))

    def delete_button_press(self):
        dialog = customtkinter.CTkInputDialog(text="Are you sure? (Y/n)", title="{} - Delete Goject".format(MAIN_WINDOW_NAME))
        value = dialog.get_input()
        if value.upper() == "Y":
            self.toplevelwindow.main_window.settings_manager.delete_goject(self.id)
            self.toplevelwindow.update_widgets_deletion()
            self.remove_all()

class GojectCheckbox(customtkinter.CTkFrame):
    def __init__(self, *args, master, name: str = "Example", status: str = "Backlog", type:str = "Goal", width: int = 100, height: int = 32, command: Callable = None, **kwargs):
        super().__init__(*args, master=master, width=width, height=height, **kwargs)
        self.type = type

        self.checkbox = customtkinter.CTkCheckBox(master, text="{}".format(name), checkbox_height=18, checkbox_width=18, font = customtkinter.CTkFont(weight="bold"), border_width=2, state=tk.DISABLED)
        self.seg_button = customtkinter.CTkSegmentedButton(master,values=["Goal", "Project"], command = self.reset_selection)
        self.status_label = customtkinter.CTkLabel(master, text="Status: {}".format(status), font = customtkinter.CTkFont(size = 10, slant="italic"), text_color=COLORS[status])        
        self.progressbar = customtkinter.CTkProgressBar(master, progress_color = "green")
        self.blank_label = customtkinter.CTkLabel(master, text=" ")

        self.seg_button.set(self.type)
        self.progressbar.set(0)

        self.checkbox.pack(anchor=tk.W)   
        self.seg_button.pack(anchor=tk.CENTER)
        self.status_label.pack(anchor=tk.CENTER)
        self.progressbar.pack(anchor=tk.CENTER)
        self.blank_label.pack(anchor=tk.W)

    def set_checkbox_value(self):
        self.checkbox.select()

    def set_progressbar_value(self, value=1):
        self.progressbar.set(value)
    
    def reset_selection(self, _):
        self.seg_button.set(self.type)

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