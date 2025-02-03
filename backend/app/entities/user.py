from datetime import date

class User:
    def __init__(self, cpf: str, name: str, profile: str, password: str):
        self.__cpf = cpf
        self.__name = name
        self.__profile = profile
        self.__password = password  # Depois vamos implementar hash

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
        return "****"  # Proteção para evitar retorno da senha em texto puro

    def set_password(self, password: str):
        self.__password = password  # Aqui depois vou usar hashing

    def check_password(self, password: str):
        return self.__password == password  # Substituir por hashing

    def __init__(self, id_client: int, street: str, city: str, neighborhood: str, complement: str):
        self.__id_client = id_client
        self.__street = street
        self.__city = city
        self.__neighborhood = neighborhood
        self.__complement = complement
    
    @property
    def id_client(self):
        return self.__id_client  # Sem setter (imutável)

    @property
    def street(self):
        return self.__street

    @street.setter
    def street(self, street: str):
        if not street.strip():
            raise ValueError("Street cannot be empty")
        self.__street = street
    
    @property
    def city(self):
        return self.__city

    @city.setter
    def city(self, city: str):
        if not city.strip():
            raise ValueError("City cannot be empty")
        self.__city = city

    @property
    def neighborhood(self):
        return self.__neighborhood

    @neighborhood.setter
    def neighborhood(self, neighborhood: str):
        if not neighborhood.strip():
            raise ValueError("neighborhood cannot be empty")
        self.__neighborhood = neighborhood
    
    @property
    def complement(self):
        return self.__complement

    @complement.setter
    def complement(self, complement: str):
        if not complement.strip():
            raise ValueError("complement cannot be empty")
        self.__complement = complement