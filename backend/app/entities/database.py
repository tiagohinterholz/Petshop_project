from datetime import date
import regex as re

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

class Breed:
    def __init__(self, description: str):
        self.__description = description
    
    @property
    def description (self):
        return self.__description
    
    @description.setter
    def description(self, description: str):
        self.__description = description

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

class Appointment:
    def __init__(self, id_pet: int, desc_appoint: str, price: float, date_appoint: date):
        self.__id_pet = id_pet
        self.__desc_appoint = desc_appoint
        self.__price = price
        self.__date_appoint = date_appoint
        
    @property
    def id_pet(self):
        return self.__id_pet
    
    @id_pet.setter
    def id_pet(self, id_pet: int):
        self.__id_pet = id_pet
    
    @property
    def desc_appoint(self):
        return self.__desc_appoint
    
    @desc_appoint.setter
    def desc_appoint(self, desc_appoint: str):
        self.__desc_appoint = desc_appoint
        
    @property
    def price(self):
        return self.__price
    
    @price.setter
    def price(self, price: float):
        if price < 0:
            raise ValueError("Price cannot be negative")
        self.__price = price
        
    @property
    def date_appoint(self):
        return self.__date_appoint
    
    @date_appoint.setter
    def date_appoint(self, date_appoint: date):
        if not isinstance(date_appointment, date):
            raise ValueError("date_appointment must be a valid date object")
        self.__date_appoint = date_appoint
        
class Client:
    def __init__(self, name: str, cpf: str, register_date: date):
        self.__name = name
        self.__cpf = cpf
        self.__register_date = register_date if register_date else date.today()
        
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name: str):
        if not name.strip():
            raise ValueError("Name cannot be empty")
        self.__name = name
        
    @property
    def cpf(self):
        return self.__cpf

    @cpf.setter
    def cpf(self, cpf: str):
        if not self.is_valid_cpf(cpf):
            raise ValueError("Invalid CPF format")
        self.__cpf = cpf
    
    @property
    def register_date(self):
        return self.__register_date
    
    @register_date.setter
    def register_date(self, register_date: date):
        if not isinstance(register_date, date):
            raise ValueError("register_date must be a valid date object")
        self.__register_date = register_date
    
    def is_valid_cpf(self, cpf: str):
        """ Validação simples de CPF (formato 000.000.000-00 ou apenas números) """
        cpf = re.sub(r"\D", "", cpf)  # Remove pontos e traços
        return len(cpf) == 11 and cpf.isdigit()  # Apenas valida comprimento e se são números

class Contact:
    VALID_TYPES = ("email", "phone")
    
    def __init__(self, id_client: int, type_contact: str, value_contact: str):
        self.__id_client = id_client
        self.__type_contact = type_contact
        self.__value_contact = value_contact
    
    @property
    def id_client(self):
        return self.__id_client
  
    @property
    def type_contact(self):
        return self.__type_contact

    @type_contact.setter
    def type_contact(self, type_contact: str):
        self.__type_contact = type_contact
    
    @property
    def value_contact(self):
        return self.__value_contact

    @value_contact.setter
    def value_contact(self, value_contact: str):
        if not value_contact.strip():
            raise ValueError("value_contact cannot be empty")

        if self.type_contact == "email":
            if not self.is_valid_email(value_contact):
                raise ValueError("Invalid email format")
        elif self.type_contact = "phone":
            if not self.is_valid_phone(value_contact):
                raise ValueError("Invalid phone number format")

        self.__value_contact = value_contact
    
    def is_valid_email(self, email: str) -> bool:
        """ Valida se o e-mail está no formato correto """
        return re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email) is not None

    def is_valid_phone(self, phone: str) -> bool:
        """ Valida se o telefone contém apenas números e tem 10 ou 11 dígitos """
        phone = re.sub(r"\D", "", phone)  # Remove caracteres não numéricos
        return len(phone) in {10, 11} and phone.isdigit()
    
class Address:
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