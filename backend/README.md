# 🐾 Petshop API

API para gerenciamento de petshop, permitindo cadastro de usuários (com perfil ADMIN e CLIENT), clientes (contato e endereço), pets, e agendamentos. Desenvolvida com Flask e PostgreSQL.

---

## 🚀 Tecnologias Utilizadas

- **Backend**: Flask (Flask-RESTful, Flask-JWT-Extended, Flask-Migrate, Flask-SQLAlchemy, Flask-Marshmallow)
- **Banco de Dados**: PostgreSQL
- **Autenticação**: JWT (JSON Web Token)
- **Testes**: Unittest
- **Containerização**: Docker (planejado para implementação futura)
- **Documentação**: Flassger (Swagger integrado ao Flask)
- **
---

## 📂 Estrutura do Projeto

```
backend/
│── backend_app/
│   ├── controller/       # Rotas da API
│   ├── docs/             # Documentação dos endpoits separados por rotas e métodos
│   ├── entities/         # Definição dos objetos das entidades
│   ├── models/           # Definição dos models do SQLAlchemy
│   ├── repository/       # Validação de ações no banco de dados
│   ├── schema_dto/       # Validação do payload da API
│   ├── services/         # Lógica das Regras de negócios
│   ├── utils/            # Funções decoradoras de proteção
│   ├── config.py         # Configurações da aplicação
│   ├── __init__.py       # Inicialização da aplicação
│── migrations/           # Migrações do banco de dados
│── tests/                # Testes unitários e de integração
│── run.py                # Ponto de entrada da aplicação
│── requirements.txt      # Dependências do projeto
│── README.md             # Documentação do projeto
```

---

## 📌 Pré-requisitos

- Python 3.12+
- PostgreSQL instalado e rodando
- Criar um banco de dados `petshop_db`

---

## 🛠️ Instalação e Configuração

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/seu-usuario/petshop-api.git
   cd petshop-api/backend
   
   ```

2. **Instalar as dependências com Poetry**:
   ```bash
   poetry install
   ```

3. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure o banco de dados de desenvolvimento** no `.env` (se aplicável) ou altere `backend_app/config.py`:
   ```python
   SQLALCHEMY_DATABASE_URI = 'postgresql://usuario:senha@localhost/petshop_db'
   ```
  **Configure o banco de dados de testes** no `.env` (se aplicável) ou altere `backend_app/config_test.py`:
   ```python
   SQLALCHEMY_DATABASE_URI = 'postgresql://usuario:senha@localhost/petshop_test'
   ```

5. **Execute as migrações do banco**:
   ```bash
   poetry run flask db upgrade
   ```

6. **Inicie a aplicação**:
   ```bash
   poetry run test
   poetry run dev
   ```

---

## 🔑 Autenticação

A autenticação é feita via **JWT**. Para obter um token:

### **📌 Login**
- **Endpoint:** `POST /login`
- **Body:**
  ```json
  {
    "cpf": "12345678900",
    "password": "sua_senha"
  }
  ```
- **Resposta:**
  ```json
  {
    "access_token": "seu_token_aqui",
    "refresh_token": "seu_refresh_token_aqui"
  }
  ```

A partir disso, utilize o token nas requisições autenticadas:
```json
Authorization: Bearer seu_token_aqui
```

### **🔄 Refresh Token**
- **Endpoint:** `POST /token/refresh`
- **Body:**
  ```json
  {
    "refresh_token": "seu_refresh_token_aqui"
  }
  ```
- **Resposta:**
  ```json
  {
    "access_token": "novo_access_token_aqui"
  }
  ```
---

## 📌 Endpoints Principais

### **Usuários**
- `POST /users` → Cria um usuário (somente perfil cliente)
- `GET /users` → Lista todos os usuários (requer permissão admin)

### **Clientes**
- `POST /clients` → Cadastra um cliente (admin ou usuário permitido)
- `GET /clients/{id}` → Busca um cliente específico (restrito)

### **Contatos**
- `POST /contacts` → Criar contato (restrito)
- `GET /contacts` → Listar contatos (restrito)

### **Endereços**
- `POST /addresses` → Criar endereço (restrito)
- `GET /addresses` → Listar endereços (restrito)

### **Pets**
- `POST /pets` → Cadastra um pet (restrito)
- `GET /pets/{id}` → Busca um pet específico (cliente autenticado)

### **Agendamentos**
- `POST /appointments` → Cria um agendamento (cliente autenticado)
- `GET /appointments` → Lista agendamentos (admin ou cliente autenticado)

### **🚪 Logout**
- **Endpoint:** `POST /logout`
- **Headers:**
  ```json
  {
    "Authorization": "Bearer seu_token_aqui"
  }

-- **Resposta**
  ```json
  {
    "detail": "Logout realizado com sucesso."
  }
```
---

## 🧪 Executando Testes

Para rodar os testes unitários, use:
```bash
python -m unittest tests/seu_arquivo.py
```

Isso garantirá que a API continua funcionando corretamente após modificações.

---

## 🚀 Próximos Passos

- 📌 Dockerizar a aplicação

---

## 📜 Licença

Este projeto está sob a licença MIT. Sinta-se à vontade para contribuir! 🐶🐱


✍️ **Autor:** Tiago F. Hinterholz