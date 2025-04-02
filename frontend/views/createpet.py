import flet as ft
import requests

def create_pet_view(page: ft.Page):
    token = page.session.get("access_token")
    user_id = page.session.get("user_id")
    
    name_input = ft.TextField(label="Nome do Pet", width=300)
    breed_dropdown = ft.Dropdown(
        label="Raça",
        width=300,
        options=[]
    )
    
    message = ft.Text(value="", color=ft.Colors.RED)

    def carregar_racas():
        try:
            response = requests.get(
                "http://localhost:5000/breeds",
                headers={"Authorization": f"Bearer {token}"}
            )
            if response.status_code == 200:
                breeds = response.json()
                breed_dropdown.options = [
                    ft.dropdown.Option(str(b["id"]), b["description"]) for b in breeds
                ]
                page.update()
            else:
                message.value = "Erro ao carregar raças"
                page.update()
        except Exception as err:
            message.value = f"Erro ao buscar raças: {err}"
            page.update()
    
    previous_route = page.session.get("previous_route") or "/create-pet"  
    if previous_route == "/create-breed":
        # Atualizar lista de raças
        carregar_racas()
        page.session.set("previous_route", None)
    
    def ir_para_cadastrar_raca(e):
        page.session.set("previous_route", "/create-pet")  # ou "/edit-pet"
        page.go("/create-breed")
    
    register_breed_btn = ft.ElevatedButton(
        text="Cadastrar nova raça",
        icon=ft.Icons.ADD,
        on_click=ir_para_cadastrar_raca
    )
    
    birth_date_input = ft.TextField(label="Data de Nascimento (AAAA-MM-DD)", width=300)

    carregar_racas()
    
    def salvar_pet(e):        
        try:
            response = requests.get(
                f"http://localhost:5000/dashboard/{user_id}",
                headers={"Authorization": f"Bearer {token}"}
            )
            if response.status_code == 200:
                client = response.json().get("client")
                client_id = client.get("id")
            else:
                message.value = "Erro ao buscar cliente."
                page.update()
                return
        
        except Exception as err:
            message.value = f"Erro: {err}"
            page.update()
            return
        
        payload = {
            "name": name_input.value,
            "birth_date": birth_date_input.value,
            "breed_id": int(breed_dropdown.value),
            "client_id": client_id    
        }
        
        try:
            response = requests.post(
                "http://localhost:5000/pets",
                json=payload,
                headers={"Authorization": f"Bearer {token}"}
            )
            
            if response.status_code == 201:
                page.go('/pets')
            else:
                message.value = f"Erro: {response.json().get('message', 'Erro Desconhecido')}"
                page.update()
        
        except Exception as err:
            message.value = f"Erro ao salvar: {err}"
            page.update()
    
    return ft.View(
        route="/create-pet",
        controls=[
            ft.Column(
                [
                    ft.Text("Cadastrar Pet", size=30, weight="bold"),
                    name_input,
                    breed_dropdown,
                    register_breed_btn,
                    birth_date_input,
                    ft.ElevatedButton("Salvar", on_click=salvar_pet),
                    ft.TextButton("Voltar", on_click=lambda e: page.go("/pets")),
                ],
                spacing=15,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True
            )
        ],
        padding=20,
        vertical_alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )