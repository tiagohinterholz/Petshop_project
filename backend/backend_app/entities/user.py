from datetime import date

class User:
    def __init__(self, cpf: str, name: str, profile: str, password: str):
        self.__cpf = cpf
        self.__name = name
        self.__profile = profile
        self.__password = password
    @property
    def cpf(self):
        return self.__cpf

    @cpf.setter
    def cpf(self, cpf: str):
        self.__cpf = cpf

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name: str):
        if not name.strip():
            raise ValueError("Name cannot be empty")
        self.__name = name

    @property
    def profile(self):
        return self.__profile

    @profile.setter
    def profile(self, profile: str):
        self.__profile = profile

    @property
    def password(self):
        return self.__password

    def set_password(self, password: str):
        self.__password = password  

    def check_password(self, password: str):
        return self.__password == password  # Substituir por hashing