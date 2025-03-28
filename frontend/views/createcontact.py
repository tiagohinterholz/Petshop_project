import flet as ft
import requests

def create_contact_view(page: ft.Page):
    token = page.session.get("access_token")
    user_id = page.session.get("user_id")  
        
    # Campos do formulário
    type_contact = ft.Dropdown(
        label="Tipo de Contato", 
        width=300,
        options=[
            ft.dropdown.Option("email"),
            ft.dropdown.Option("telefone")
        ]
    )
    value_contact = ft.TextField(label="Dados", width=300)
    message = ft.Text(value="", color=ft.colors.RED)
    
    def formatar_telefone(e):
        numero = ''.join(filter(str.isdigit, value_contact.value))[:13]
        if len(numero) >= 12:
            formatado = f"({numero[:2]})-{numero[2:7]}-{numero[7:]}"
        elif len(numero) >= 7:
            formatado = f"({numero[:2]})-{numero[2:7]}-{numero[7:]}"
        elif len(numero) >= 2:
            formatado = f"({numero[:2]})-{numero[2:]}"
        else:
            formatado = numero

        value_contact.value = formatado
        page.update()
    
    def on_value_change(e):
        if type_contact.value == "telefone":
            formatar_telefone(e)
    
    def ao_mudar_tipo(e):
        value_contact.value = ""
        page.update()
    
    value_contact.on_change = on_value_change
    type_contact.on_change = ao_mudar_tipo
    
    def salvar_contato(e):
        try:
            response = requests.get(
                f"http://localhost:5000/dashboard/{user_id}",
                headers={"authorization": f"Bearer {token}"}
            )
            if response.status_code == 200:
                client = response.json().get("client")
                client_id = client.get("id")
            else:
                message.value = "Cliente não encontrado."
                page.update()
                return
        except Exception as err:
            message.value = f"Erro ao buscar cliente: {err}"
            page.update()
            return
        
        payload = {
            "client_id": client_id,
            "type_contact": type_contact.value,
            "value_contact": value_contact.value,            
        }
        
        try:
            response = requests.post(
                "http://localhost:5000/contacts",
                json=payload,
                headers={"authorization": f"Bearer {token}"}
            )
            if response.status_code == 201:
                page.go("/profile")
            else:
                message.value = f"Erro ao salvar: {response.json().get('message', 'Erro desconhecido')}"
                page.update()
        except Exception as err:
            message.value = f"Erro de conexão: {err}"
            page.update()
        
    return ft.View(
        route="/create-contact",
        controls=[
            ft.Column(
                [
                    ft.Text("Cadastrar Contato", size=30, weight="bold"),
                    type_contact,
                    value_contact,
                    ft.ElevatedButton("Salvar", on_click=salvar_contato),
                    ft.TextButton("Voltar", on_click=lambda e: page.go("/profile")),
                    message
                ],
                spacing=15,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )