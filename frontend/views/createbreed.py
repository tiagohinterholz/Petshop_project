import flet as ft
import requests

def create_breed_view(page: ft.Page):
    token = page.session.get("access_token")
    previous_route = page.session.get("previous_route") or "/create-pet" 
    
    description = ft.TextField(label="Descrição da raça", width=300, autofocus=True)
    message = ft.Text(value="", color=ft.Colors.RED)
    
    def salvar_breed(e):
    
        payload = {
            "description": description.value
        }
        
        try:
            response = requests.post(
                "http://localhost:5000/breeds",
                json=payload,
                headers={"Authorization": f"Bearer {token}"}
            )
            if response.status_code == 201:
                page.go(previous_route)
            else:
                data = response.json()
                message.value = f"Erro: {data.get('error', 'Erro desconhecido')}"
                page.update()
                
        except Exception as err:
            message.value = f"Erro: {err}"
            page.update()
    
    return ft.View(
        route = '/create-breed',
        controls=[
            ft.Column(
                [
                    ft.Text("Cadastrar Raça", size=30, weight="bold"),
                    description,
                    ft.ElevatedButton("Salvar", on_click=salvar_breed),
                    ft.TextButton("Voltar", on_click=lambda e: page.go(previous_route)),
                    message
                ],
                spacing=20,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER
            )
        ],
        vertical_alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        padding=20
    )