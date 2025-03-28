import flet as ft
import requests

def edit_address_view(page: ft.Page):
    token = page.session.get("access_token")
    user_id = page.session.get("user_id")

    # TextFields com "disabled" inicialmente
    street = ft.TextField(label="Rua", width=300, disabled=True)
    city = ft.TextField(label="Cidade", width=300, disabled=True)
    neighborhood = ft.TextField(label="Bairro", width=300, disabled=True)
    complement = ft.TextField(label="Complemento", width=300, disabled=True)
    message = ft.Text(value="", color=ft.colors.RED)

    # Checkboxes para habilitar edição
    cb_street = ft.Checkbox(label="Editar Rua", value=False)
    cb_city = ft.Checkbox(label="Editar Cidade", value=False)
    cb_neighborhood = ft.Checkbox(label="Editar Bairro", value=False)
    cb_complement = ft.Checkbox(label="Editar Complemento", value=False)

    def toggle_field(field, checkbox):
        field.disabled = not checkbox.value
        page.update()

    cb_street.on_change = lambda e: toggle_field(street, cb_street)
    cb_city.on_change = lambda e: toggle_field(city, cb_city)
    cb_neighborhood.on_change = lambda e: toggle_field(neighborhood, cb_neighborhood)
    cb_complement.on_change = lambda e: toggle_field(complement, cb_complement)

    def carregar_endereco():
        try:
            response = requests.get(
                f"http://localhost:5000/dashboard/{user_id}",
                headers={"authorization": f"Bearer {token}"}
            )
            if response.status_code == 200:
                address = response.json().get("address")
                if address:
                    street.value = address.get("street", "")
                    city.value = address.get("city", "")
                    neighborhood.value = address.get("neighborhood", "")
                    complement.value = address.get("complement", "")
                    page.update()
                else:
                    message.value = "Endereço não encontrado."
                    page.update()
        except Exception as err:
            message.value = f"Erro ao buscar endereço: {err}"
            page.update()

    def atualizar_endereco(e):
        payload = {}
        if cb_street.value:
            payload["street"] = street.value
        if cb_city.value:
            payload["city"] = city.value
        if cb_neighborhood.value:
            payload["neighborhood"] = neighborhood.value
        if cb_complement.value:
            payload["complement"] = complement.value

        if not payload:
            message.value = "Selecione pelo menos um campo para atualizar."
            page.update()
            return

        try:
            dashboard = requests.get(
                f"http://localhost:5000/dashboard/{user_id}",
                headers={"authorization": f"Bearer {token}"}
            )
            address = dashboard.json().get("address")
            address_id = address.get("id")

            response = requests.put(
                f"http://localhost:5000/addresses/{address_id}",
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

    carregar_endereco()

    return ft.View(
        route="/edit-address",
        controls=[
            ft.Column(
                [
                    ft.Text("Editar Endereço", size=30, weight="bold"),
                    cb_street,
                    street,
                    cb_city,
                    city,
                    cb_neighborhood,
                    neighborhood,
                    cb_complement,
                    complement,
                    ft.ElevatedButton("Salvar Alterações", on_click=atualizar_endereco),
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
