import os, json
from typing import List

from src.goject import Goject
from src.config import *

class FileManager():
    def __init__(self):
        self.__local_path = os.getcwd()
        self.__data = {"gojects": []}

    def load_gojects(self):
        gojects_list = []

        if not os.path.exists("./data/gojects.json"):
            try:
                os.mkdir(os.path.join(str(self.__local_path), "data"))
            except:
                print("Pasta de dados já existe, criando arquivo gojects.json...")
            with open("./data/gojects.json", "w") as write_file:
                json.dump(self.__data, write_file, ensure_ascii=False, indent=2, )
        else:    
            with open("./data/gojects.json") as json_file:
                self.__data = json.load(json_file)

        for goject in self.__data["gojects"]:
            new_goject = Goject(goject[0], goject[1], goject[2], goject[3], goject[4], goject[5], goject[6])
            gojects_list.append(new_goject)

        return gojects_list

    def save_gojects(self, gojects_list: List[Goject]):
        self.__data = {"gojects": []}
        for goject in gojects_list:
            self.__data["gojects"].append([goject.id, goject.name, goject.type, goject.status, TOPICS[goject.topic], goject.due_date, goject.parent])
        with open("./data/gojects.json", "w") as write_file:
            json.dump(self.__data, write_file, ensure_ascii=False, indent=2)

    def file_manager(self, dir_record="Gojects", dir_goject_name="videos"):
        save_dir = "./data/{}/{}/".format(dir_record, dir_goject_name)
        if not os.path.exists(save_dir):
            print("Não exite caminho para salvar. Criando...")
            try:
                os.mkdir(os.path.join(str(self.__local_path), "data", dir_record))
            except:
                print("Pasta do {} já existente, criando a {}...".format(dir_record, dir_goject_name))
            os.mkdir(save_dir)
        else:
            print("Pasta existe. Salvando em diretório já existente")
        return save_dir

    def file_cleaner(self, save_dir):
        "Required and wanted processing of final files"

        if os.path.exists(save_dir + "temp_audio.wav"):
            os.remove(save_dir + "temp_audio.wav")
        if os.path.exists(save_dir + "temp_video.avi"):
            os.remove(save_dir + "temp_video.avi")
        if os.path.exists(save_dir + "temp_video2.avi"):
            os.remove(save_dir + "temp_video2.avi")
        # if os.path.exists(str(local_path) + "/" + filename + ".avi"):
        #     os.remove(str(local_path) + "/" + filename + ".avi")

class SettingsManager:
    def __init__(self, file_manager: FileManager) -> None:
        self.__file_manager = file_manager
        self.__goject_buffer = file_manager.load_gojects()
        self.__projects = []
        self.__goals = []
        self.__goject_counter = len(self.__goject_buffer)
        self.__number_goals = 0
        self.__number_projects = 0

        for goject in self.__goject_buffer:
            if goject.type == "Goal":
                self.__goals.append(goject)
                self.__number_goals += 1
            elif goject.type == "Project":
                self.__projects.append(goject)
                self.__number_projects += 1
            else:
                print("{} has wrong type name, please edit".format(goject.name))
        self.show_count_status()

    @property
    def goject_buffer(self):
        return self.__goject_buffer

    @property
    def projects(self):
        return self.__projects
    
    @property
    def goals(self):
        return self.__goals

    @property
    def number_goals(self):
        return self.__number_goals

    @property
    def number_projects(self):
        return self.__number_projects

    @property
    def goject_counter(self):
        return self.__goject_counter

    @goject_buffer.setter
    def goject_buffer(self, gojects_list):
        self.__goject_buffer = gojects_list
        self.save_gojects()

    def create_goject(self, name, type, status, topic, due_date="", parent=None):
        new_goject = Goject(self.__goject_counter, name, type, status, topic, due_date, parent)
        self.__goject_counter += 1
        if type == "Goal":
            self.__goals.append(new_goject)
            self.__number_goals += 1
        elif type == "Project":
            self.__projects.append(new_goject)
            self.__number_projects += 1
        self.__goject_buffer.append(new_goject)
        self.save_gojects()
    
    def alter_goject(self, id, property, new_value):
        if property == "name":
            self.__goject_buffer[id].name = new_value
        elif property == "status":
            self.__goject_buffer[id].status = new_value
        elif property == "due_date": 
            self.__goject_buffer[id].due_date = new_value
        elif property == "topic":
            self.__goject_buffer[id].topic = new_value
        elif property == "parent":
            self.__goject_buffer[id].parent = self.__goject_buffer[new_value]
        else:
            #TO DO: pop up warning window
            print("Sorry, Gabe. I'm afraid you can't alter {}".format(property))
            return
        self.save_gojects()

    def delete_goject(self, id):
        #TO DO: verify if operation can be done with the index
        type = self.__goject_buffer[id].type
        del self.__goject_buffer[id]
        if type == "Goal":
            self.__number_goals -= 1
        elif type == "Project":
            self.__number_projects -= 1
        self.__goject_counter -= 1
        #resets the following gojects' id to not mess up the counter
        for goject in self.__goject_buffer[id:]:
            goject.id -= 1
        self.reset_buffers()
        self.save_gojects()
    
    def reset_buffers(self):
        self.__projects = []
        self.__goals = []
        for goject in self.__goject_buffer:
            if goject.type == "Goal":
                self.__goals.append(goject)
            elif goject.type == "Project":
                self.__projects.append(goject)
            else:
                print("{} has wrong type name, please edit".format(goject.name))

        self.__number_goals = len(self.__goals)
        self.__number_projects = len(self.__projects)

    def save_gojects(self):
        self.show_count_status()
        self.__file_manager.save_gojects(self.__goject_buffer)

    def show_count_status(self):
        print("{} Gojects loaded: {} Goals and {} Projects".format(self.__goject_counter, self.__number_goals, self.__number_projects))

    def confirm_operation(self, message):
        confirmation = False
        #TO DO: create a pop up to confirm del and creation
        return confirmation

if __name__ == '__main__':
    file = FileManager()
    manager = SettingsManager(file)
    
    manager.create_goject("Main Void", "Goal", "Backlog", "ARTIFICIAL_INTELLIGENCE")
    manager.create_goject("Research Scientist at Big Tech", "Goal", "Backlog", "ARTIFICIAL_INTELLIGENCE")
    manager.create_goject("PhD", "Goal", "Backlog", "ARTIFICIAL_INTELLIGENCE")
    manager.create_goject("Kaggle Grandmaster", "Goal", "Backlog", "ARTIFICIAL_INTELLIGENCE")
    manager.create_goject("ICPC", "Goal", "Backlog", "PROGRAMMING")
    manager.create_goject("PIC", "Goal", "Backlog", "ARTIFICIAL_INTELLIGENCE")
    manager.create_goject("PIX Internship", "Goal", "Backlog", "ARTIFICIAL_INTELLIGENCE")
    manager.create_goject("College", "Goal", "Backlog", "COMPUTER_SCIENCE")
    manager.create_goject("Three Languages", "Goal", "Backlog", "LANGUAGES")
    manager.create_goject("80KG Calisthenics", "Goal", "Backlog", "SPORTS_HEALTH")
    manager.create_goject("Voluntariado", "Goal", "Backlog", "ENTREPRENEURSHIP")
    manager.create_goject("Non-Fiction Book", "Goal", "Backlog", "WRITING")
    manager.create_goject("Write with left hand", "Goal", "Backlog", "WRITING")
    manager.create_goject("Personal Website", "Goal", "Backlog", "PROGRAMMING")
    manager.create_goject("Finance", "Goal", "Backlog", "FINANCE")
    manager.create_goject("Live Loops", "Goal", "Backlog", "MUSIC")
    manager.create_goject("Orquestra", "Goal", "Backlog", "MUSIC")
    manager.create_goject("80 books", "Goal", "Backlog", "BOOKS")
    manager.create_goject("Visual Poetry", "Goal", "Backlog", "PHOTOGRAPHY_DESIGN")
    manager.create_goject("Imagetic References", "Goal", "Backlog", "DRAWING_PAINTING")
    manager.create_goject("Mindful Digressions", "Goal", "Backlog", "PHOTOGRAPHY_DESIGN")
    manager.create_goject("3 Sci-fi Books", "Goal", "Backlog", "WRITING")
    manager.create_goject("Graphic Novel", "Goal", "Backlog", "PHOTOGRAPHY_DESIGN")
    manager.create_goject("Game", "Goal", "Backlog", "PROGRAMMING")
    manager.create_goject("Art House", "Goal", "Backlog", "PHOTOGRAPHY_DESIGN")