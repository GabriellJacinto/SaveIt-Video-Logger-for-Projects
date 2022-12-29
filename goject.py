class Goject:
    def __init__(self, id, name, type, status, due_date=None) -> None:
        self.__id = id
        self.__name = name
        self.__type = type
        self.__due_date = due_date
        self.__status = status
    
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
    