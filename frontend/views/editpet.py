import flet as ft
import requests

def edit_pet_view(page: ft.Page):

    token = page.session.get("access_token")
    user_id = page.session.get("user_id")

    # TextFields com "disabled" inicialmente
    name = ft.TextField(label="Nome", width=300, disabled=True)
    birth_date = ft.TextField(label="Data de nascimento", width=300, disabled=True)
    breed_dropdown = ft.Dropdown(
        label="Raça",
        width=300,
        options=[],
        disabled=True
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
    
    previous_route = page.session.get("previous_route")
    if previous_route == "/create-breed":
        # Atualizar lista de raças
        carregar_racas()
        page.session.set("previous_route", None)

    
    # Checkboxes para habilitar edição
    cb_name = ft.Checkbox(label="Editar Nome", value=False)
    cb_birth_date = ft.Checkbox(label="Editar Data de Nascimeto", value=False)
    cb_breed = ft.Checkbox(label="Editar Raça", value=False)
    
    def toggle_field(field, checkbox):
        field.disabled = not checkbox.value
        page.update()

    cb_name.on_change = lambda e: toggle_field(name, cb_name)
    cb_birth_date.on_change = lambda e: toggle_field(birth_date, cb_birth_date)
    cb_breed.on_change = lambda e: toggle_field(breed_dropdown, cb_breed)
    
    def ir_para_cadastrar_raca(e):
        page.session.set("previous_route", page.route)  # ou "/edit-pet"
        page.go("/create-breed")
    
    register_breed_btn = ft.ElevatedButton(
        text="Cadastrar nova raça",
        icon=ft.Icons.ADD,
        on_click=ir_para_cadastrar_raca
    )

    def carregar_pet():
        try:           
            response = requests.get(
                f"http://localhost:5000/dashboard/{user_id}",
                headers={"Authorization": f"Bearer {token}"}
            )
            if response.status_code == 200:
                pets = response.json().get("pets", [])
                pet_id = int(page.route.split("?id=")[-1])
                pet = next((p for p in pets if p["id"] == pet_id), None)
                if pet:
                    name.value = pet.get("name", "")
                    birth_date.value = pet.get("birth_date", "")
                    breed_dropdown.value = str(pet.get("breed_id"))
                    page.update()
                else:
                    message.value = "Pet não encontrado."
                    page.update()
        except Exception as err:
            message.value = f"Erro ao buscar pet: {err}"
            page.update()

    def atualizar_pet(e):
        dashboard = requests.get(
            f"http://localhost:5000/dashboard/{user_id}",
            headers={"authorization": f"Bearer {token}"}
        )
        client_id = dashboard.json().get("client", {}).get("id")
        
        payload = {}
        
        payload["client_id"] = client_id
        
        if cb_name.value:
            payload["name"] = name.value
        if cb_birth_date.value:
            payload["birth_date"] = birth_date.value
        if cb_breed.value and breed_dropdown.value:
            payload["breed_id"] = int(breed_dropdown.value)

        if not payload:
            message.value = "Selecione pelo menos um campo para atualizar."
            page.update()
            return

        try:
            pet_id = int(page.route.split("?id=")[-1])  # <-- aqui está a correção
            response = requests.put(
                f"http://localhost:5000/pets/{pet_id}",
                json=payload,
                headers={"Authorization": f"Bearer {token}"}
            )
            if response.status_code == 200:
                page.go("/pets")
            else:
                message.value = f"Erro ao atualizar: {response.json().get('message', 'Erro desconhecido')}"
                page.update()
        except Exception as err:
            message.value = f"Erro de conexão: {err}"
            page.update()

    carregar_racas()
    carregar_pet()

    return ft.View(
        route="/edit-pet",
        controls=[
            ft.Column(
                [
                    ft.Text("Editar Pet", size=30, weight="bold"),
                    cb_name,
                    name,
                    cb_birth_date,
                    birth_date,
                    cb_breed,
                    breed_dropdown,
                    register_breed_btn,
                    ft.ElevatedButton("Salvar Alterações", on_click=atualizar_pet),
                    ft.TextButton("Voltar", on_click=lambda e: page.go("/pets")),
                    message
                ],
                spacing=10,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
