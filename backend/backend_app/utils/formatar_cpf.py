import re

def formatar_cpf(cpf):
    """Formata CPF para padrão 000.000.000-00"""
    cpf = re.sub(r"\D", "", cpf)  # Remove tudo que não for número
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}" if len(cpf) == 11 else cpf