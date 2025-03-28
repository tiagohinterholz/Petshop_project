import flet as ft
import requests

def create_address_view(page: ft.Page):
    token = page.session.get("access_token")
    user_id = page.session.get("user_id")
    
    # Campos do formulário
    street = ft.TextField(label="Rua", width=300)
    city = ft.TextField(label="Cidade", width=300)
    neighborhood = ft.TextField(label="Bairro", width=300)
    complement = ft.TextField(label="Complemento", width=300)
    message = ft.Text(value="", color=ft.colors.RED)
    
    def salvar_endereco(e):
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
            "street": street.value,
            "city": city.value,
            "neighborhood": neighborhood.value,
            "complement": complement.value
        }
        
        try:
            response = requests.post(
                "http://localhost:5000/addresses",
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
        route="/create-address",
        controls=[
            ft.Column(
                [
                    ft.Text("Cadastrar Endereço", size=30, weight="bold"),
                    street,
                    city,
                    neighborhood,
                    complement,
                    ft.ElevatedButton("Salvar", on_click=salvar_endereco),
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
            