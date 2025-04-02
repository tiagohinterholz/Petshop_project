# 🐾 Petshop Frontend

Interface gráfica para o sistema de gerenciamento de petshop, construída com **Flet** (Python), oferecendo funcionalidades completas para usuários e administradores interagirem com pets, agendamentos, clientes e mais.

---

## 🚀 Tecnologias Utilizadas

- **Frontend**: [Flet](https://flet.dev/)
- **Linguagem**: Python 3.12+
- **UI Dinâmica**: Baseada em Views e Componentes
- **Requisições REST**: Integração com API Flask via `requests`
- **Controle de Sessão**: Utiliza `page.session`
- **Design Responsivo**: Layouts adaptáveis com `Row`, `Column` e `Container`

---

## 📂 Estrutura do Projeto

```
frontend/
│── auth/                  # Login e controle de autenticação
│── components/            # Componentes reutilizáveis como header e sidebar
│── views/                 # Páginas principais (Dashboard, Pets, Profile, etc)
│── main.py                # Arquivo principal com rotas e inicialização
│── README.md              # Documentação do projeto
```

---

## 📌 Pré-requisitos

- Python 3.12+
- Backend rodando localmente (http://localhost:5000)
- Biblioteca Flet instalada

---

## 🛠️ Instalação e Execução

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/seu-usuario/petshop-frontend.git
   cd petshop-frontend/frontend
   ```

2. **Instale as dependências com poetry**:
   ```bash
   poetry install
   ```

3. **Execute a aplicação**:
   ```bash
   flet run main.py
   ```

---

## 🔐 Autenticação

- A autenticação é feita via **JWT**, herdando o token obtido no login do backend.
- O token é salvo em `page.session["access_token"]` e enviado em todas as requisições REST.

---

## 📌 Funcionalidades

### 👤 Usuários
- Login com CPF e senha
- Criação de novos usuários (admin → cliente)

### 🐶 Pets
- Cadastro, edição e exclusão de pets
- Visualização com cards
- Vínculo com agendamentos

### 📆 Agendamentos
- Agendamentos futuros visíveis na dashboard
- Tela completa para agendar e editar serviços

### 🧾 Perfil
- Visualização e edição de contato e endereço
- Registro de cliente (caso ainda não exista)
- Layout em colunas com responsividade

---

## 📅 Próximas Funcionalidades

- Calendário interativo para escolha de dias e horários de agendamento
- Notificações visuais para serviços futuros
- Organização visual por tipos de usuário

---

## 🧪 Testes

Ainda não implementado no frontend, mas planejado com `pytest + flet_test`.

---

## 📜 Licença

Este projeto está sob a licença MIT. Contribuições são bem-vindas! 🐕🧼

✍️ **Autor:** Tiago F. Hinterholz
