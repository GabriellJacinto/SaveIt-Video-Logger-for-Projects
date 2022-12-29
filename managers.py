import os, json
from typing import List

from goject import Goject

class FileManager():
    def __init__(self):
        self.__local_path = os.getcwd()
        self.__data = {"gojects": []}

    def load_gojects(self):
        gojects_list = []
        if not os.path.exists(str(self.__local_path) + "/gojects.json"):
            with open("gojects.json", "w") as write_file:
                json.dump(self.__data, write_file, ensure_ascii=False, indent=2)
        else:    
            with open("gojects.json") as json_file:
                self.__data = json.load(json_file)
        for goject in self.__data["gojects"]:
            new_goject = Goject(goject[0], goject[1], goject[2], goject[3], goject[4])
            gojects_list.append(new_goject)
        return gojects_list

    def save_gojects(self, gojects_list: List[Goject]):
        self.__data = {"gojects": []}
        for goject in gojects_list:
            self.__data["gojects"].append([goject.id, goject.name, goject.type, goject.status, goject.due_date])
        with open("gojects.json", "w") as write_file:
            json.dump(self.__data, write_file, ensure_ascii=False, indent=2)

    def file_manager(self):
        "Required and wanted processing of final files"
        
        if os.path.exists(str(self.__local_path) + "/temp_audio.wav"):
            os.remove(str(self.__local_path) + "/temp_audio.wav")
        if os.path.exists(str(self.__local_path) + "/temp_video.avi"):
            os.remove(str(self.__local_path) + "/temp_video.avi")
        if os.path.exists(str(self.__local_path) + "/temp_video2.avi"):
            os.remove(str(self.__local_path) + "/temp_video2.avi")
        # if os.path.exists(str(local_path) + "/" + filename + ".avi"):
        #     os.remove(str(local_path) + "/" + filename + ".avi")

class SettingsManager:
    def __init__(self, file_manager: FileManager) -> None:
        self.__file_manager = file_manager
        self.__goject_buffer = file_manager.load_gojects()
        self.__goject_counter = len(self.__goject_buffer)

    @property
    def goject_buffer(self):
        return self.__goject_buffer

    @goject_buffer.setter
    def goject_buffer(self, gojects_list):
        self.__goject_buffer = gojects_list
        self.save_gojects()
    
    def create_goject(self, name, type, status, due_date=None):
        new_goject = Goject(self.__goject_counter, name, type, status, due_date)
        self.__goject_counter += 1
        self.__goject_buffer.append(new_goject)
        self.save_gojects()
    
    def alter_goject(self, id, property, new_value):
        if property == "name":
            self.__goject_buffer[id].name = new_value
        elif property == "status":
            self.__goject_buffer[id].status = new_value
        elif property == "due_date": 
            self.__goject_buffer[id].due_date = new_value
        else:
            #pop up warning
            print("Sorry, Gabe. I'm afraid you can't alter {}".format(property))
            return
        self.save_gojects()

    def delete_goject(self, id):
        #verificar se operacao é possivel de ser feita
        del self.__goject_buffer[id]
        self.__goject_counter -= 1
        #reset the following gojects' id to not mess up the counter
        for goject in self.__goject_buffer[id:]:
            goject.id -= 1
        self.save_gojects()
    
    def save_gojects(self):
        self.__file_manager.save_gojects(self.__goject_buffer)

    def confirm_operation(self, message):
        confirmation = False
        #create a pop up to confirm del and creation
        return confirmation

if __name__ == '__main__':
    file = FileManager()
    manager = SettingsManager(file)
    
    #manager.create_goject("carpeDiem", "Goal", "Backlog")
    manager.create_goject("carpe on them Diem", "Project", "Backlog", "2011")
    #manager.create_goject("Diem capado", "Goal", "In progress", "Jul 2020")
    
    #manager.alter_goject(0,"type","Project")
    #manager.alter_goject(2,"status", "ACABOU não é hexa :'(")
    #manager.alter_goject(0,"due_date","Aug 2900")
    #manager.alter_goject(1,"name","Diem CAPADO mesmo")
    
    #manager.delete_goject(0)
    #manager.create_goject("Diem sim", "Goal", "In progress")
    
    manager.save_gojects()