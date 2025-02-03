from datetime import date
import regex as re

class Breed:
    def __init__(self, description: str):
        self.__description = description
    
    @property
    def description (self):
        return self.__description
    
    @description.setter
    def description(self, description: str):
        self.__description = description
