from datetime import date
import regex as re

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
        elif self.type_contact == "phone":
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
    
