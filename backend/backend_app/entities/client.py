from datetime import date
import regex as re
        
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