from datetime import date
import regex as re

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
        if not isinstance(date_appoint, date):
            raise ValueError("date_appointment must be a valid date object")
        self.__date_appoint = date_appoint