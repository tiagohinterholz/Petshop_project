# 🐾 Petshop Manager - Sistema Completo

Bem-vindo ao **Petshop Manager**, um sistema completo de gerenciamento para petshops, unindo frontend interativo com backend robusto.  
Este projeto foi desenvolvido com foco em facilitar o controle de clientes, pets, agendamentos e usuários administrativos.

---

## 📦 Estrutura do Projeto

Este repositório é dividido em duas partes principais:

```
petshop_project/
│
├── frontend/   # Interface gráfica com Flet (Python)
│   └── README.md
│
├── backend/    # API RESTful com Flask + PostgreSQL
│   └── README.md
```

Cada uma dessas pastas contém um `README.md` com instruções específicas.

---

## 🚀 Tecnologias Utilizadas

### Backend
- **Flask** + Flask-RESTful, Flask-JWT-Extended, Flask-SQLAlchemy
- **PostgreSQL**
- **Autenticação JWT**
- **Swagger UI**
- **Testes com Unittest**

### Frontend
- **Flet (Python)**
- Interface responsiva com controle de sessão
- Comunicação com a API via `requests`
- Navegação por views e componentes reutilizáveis

---

## 💻 Funcionalidades Gerais

- **Autenticação de usuários** (admin e cliente)
- **Cadastro e gerenciamento de pets**
- **Agendamento de serviços** com controle de tempo
- **Dashboard com dados dinâmicos**
- **Gestão de contatos e endereços**
- **Calendário inteligente para agendamentos** *(em desenvolvimento)*

---

## 🧭 Como Executar

### 🔧 Backend
```bash
cd backend
poetry install
poetry run flask db upgrade
poetry run test - Para testes em banco de dados
poetry run dev - Para banco de dados em desenvolvimento
```

### 🖥️ Frontend
```bash
cd frontend
poetry install
flet run main.py
```

---

## 📸 Screenshots (em breve)

Imagens da interface e funcionalidades do sistema em uso.

---

## 📜 Licença

Projeto sob a licença MIT. Contribuições são bem-vindas! 😄

✍️ **Autor:** Tiago F. Hinterholz
