from datetime import date

class Pet:
    def __init__(self, id_client: int, id_breed: int, birth_date: date, name: str):
        self.__id_client = id_client
        self.__id_breed = id_breed
        self.__birth_date = birth_date
        self.__name = name
    
    @property
    def id_client(self):
        return self.__id_client
    
    @id_client.setter
    def id_client(self, id_client: int):
        self.__id_client = id_client
    
    @property
    def id_breed(self):
        return self.__id_breed
    
    @id_breed.setter
    def id_breed(self, id_breed: int):
        self.__id_breed = id_breed
    
    @property
    def birth_date(self):
        return self.__birth_date
    
    @birth_date.setter
    def birth_date(self, birth_date: date):
        if not isinstance(birth_date, date):
            raise ValueError("birth_date must be a valid date object")
        self.__birth_date = birth_date
    
    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, name):
        self.__name = name