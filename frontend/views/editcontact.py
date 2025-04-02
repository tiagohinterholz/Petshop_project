import flet as ft
import requests

def edit_contact_view(page: ft.Page):
    token = page.session.get("access_token")
    user_id = page.session.get("user_id")
    
    # TextFields com "disabled" inicialmente
    type_contact = ft.Dropdown(
        label="Tipo de Contato", 
        width=300,
        options=[
            ft.dropdown.Option("email"),
            ft.dropdown.Option("telefone")
        ],
        disabled=True
    )
    value_contact = ft.TextField(label="Dados", width=300, disabled=True)
    message = ft.Text(value="", color=ft.Colors.RED)

    # Checkboxes para habilitar edição
    cb_type = ft.Checkbox(label="Editar Tipo de Contato", value=False)
    cb_value = ft.Checkbox(label="Editar Dados de Contato", value=False)
    
    def toggle_field(field, checkbox):
        field.disabled = not checkbox.value
        page.update()

    cb_type.on_change = lambda e: toggle_field(type_contact, cb_type)
    cb_value.on_change = lambda e: toggle_field(value_contact, cb_value)
    
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
    
    def carregar_contato():
        try:
            response = requests.get(
                f"http://localhost:5000/dashboard/{user_id}",
                headers={"authorization": f"Bearer {token}"}
            )
            if response.status_code == 200:
                contact = response.json().get("contact")
                if contact:
                    type_contact.value = contact.get("type_contact", "")
                    value_contact.value = contact.get("value_contact", "")
                    page.update()
                else:
                    message.value = "Contato não encontrado."
                    page.update()
        except Exception as err:
            message.value = f"Erro ao buscar Contato: {err}"
            page.update()

    def atualizar_contato(e):
        payload = {}
        
        if cb_type.value:
            payload["type_contact"] = type_contact.value
        if cb_value.value:
            payload["value_contact"] = value_contact.value
        
        if not payload:
            message.value = "Selecione pelo menos um campo para atualizar."
            page.update()
            return
        
        try:
            dashboard = requests.get(
                f"http://localhost:5000/dashboard/{user_id}",
                headers={"authorization": f"Bearer {token}"}
            )
            contact = dashboard.json().get("contact")
            contact_id = contact.get("id")
            client_id = contact.get("client_id")
            payload["client_id"] = client_id

            response = requests.put(
                f"http://localhost:5000/contacts/{contact_id}",
                json=payload,
                headers={"authorization": f"Bearer {token}"}
            )

            if response.status_code == 200:
                page.go("/profile")
            else:
                message.value = f"Erro ao atualizar: {response.json().get('message', 'Erro desconhecido')}"
                page.update()
        except Exception as err:
            message.value = f"Erro de conexão: {err}"
            page.update()

    carregar_contato()

    return ft.View(
        route="/edit-contact",
        controls=[
            ft.Column(
                [
                    ft.Text("Editar Contato", size=30, weight="bold"),
                    cb_type,
                    cb_value,
                    type_contact,
                    value_contact,
                    ft.ElevatedButton("Salvar Alterações", on_click=atualizar_contato),
                    ft.TextButton("Voltar", on_click=lambda e: page.go("/profile")),
                    message
                ],
                spacing=10,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
