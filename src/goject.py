from enum import Enum, auto

class Topic(Enum):
    BOOKS = auto()
    ARTIFICIAL_INTELLIGENCE = auto()
    PROGRAMMING = auto()
    COMPUTER_SCIENCE = auto()
    MATHEMATICS = auto()
    NEUROSCIENCE = auto()
    ELECTRONIC = auto()
    QUANTUM_PHYSICS = auto()
    MUSIC = auto()
    PHOTOGRAPHY_DESIGN = auto()
    DRAWING_PAINTING = auto()
    WRITING = auto()
    SPORTS_HEALTH = auto()
    FINANCE = auto()
    ENTREPRENEURSHIP = auto()
    LANGUAGES = auto()

class Goject:
    def __init__(self, id, name, type, status, topic: Topic, due_date=None, parent=None) -> None:
        self.__id = id
        self.__name = name
        self.__type = type
        self.__due_date = due_date
        self.__status = status
        self.__parent = parent
        self.__topic = topic
    
    @property
    def parent(self):
        return self.__parent

    @property
    def topic(self):
        return self.__topic

    @property
    def status(self):
        return self.__status
    
    @property
    def id(self):
        return self.__id
    
    @property
    def name(self):
        return self.__name
    
    @property
    def due_date(self):
        return self.__due_date

    @property
    def type(self):
        return self.__type

    @parent.setter
    def parent(self, parent):
        pass

    @topic.setter
    def topic(self, topic):
        self.__topic = topic

    @id.setter
    def id(self, id):
        self.__id = id

    @status.setter
    def status(self, status):
        self.__status = status
    
    @name.setter
    def name(self, name):
        self.__name = name
    
    @due_date.setter
    def due_date(self, due_date):
        self.__due_date = due_date

if __name__ == '__main__':
    teste = Goject(10, "Carpe diem", "Goal", "Backlog", "2100")
    print(teste.name)
    print(teste.type)
    print(teste.status)
    teste.status = "In Progress"
    print(teste.status)
    print(teste.id)
    teste.id -= 10
    print(teste.id)