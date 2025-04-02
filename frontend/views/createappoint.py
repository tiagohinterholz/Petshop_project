import flet as ft
import requests

def create_appointments_view(page: ft.Page):
    token = page.session.get("access_token")
    user_id = page.session.get("user_id")

    try:
        response = requests.get(
            f"http://localhost:5000/dashboard/{user_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        if response.status_code == 200:
            pets = response.json().get("pets", [])
    except:
        pets = []

    try:
        response = requests.get(
            f"http://localhost:5000/procedures",
            headers={"Authorization": f"Bearer {token}"}
        )
        if response.status_code == 200:
            procedures = response.json()
    except:
        procedures = []

    date_appoint = ft.TextField(label="Data escolhida (AAAA-MM-DD)", width=300)

    time_text = ft.Text(value="Horário não selecionado")

    time_picker = ft.TimePicker(
        confirm_text="OK",
        cancel_text="Cancelar",
        help_text="Selecione o horário",
        on_change=lambda e: (
            time_text.__setattr__('value', f"{str(e.control.value)[:5]}")
            or page.update()
        )
    )

    page.overlay.append(time_picker)

    time_btn = ft.ElevatedButton(
        text="Selecionar Horário",
        on_click=lambda _: page.open(time_picker)
    )

    pet_dropdown = ft.Dropdown(
        label="Pet",
        width=300,
        options=[ft.dropdown.Option(text=pet["name"], key=str(pet["id"])) for pet in pets]
    )

    procedure_dropdown = ft.Dropdown(
        label="Serviço",
        width=300,
        options=[ft.dropdown.Option(text=p["name"], key=str(p["id"])) for p in procedures]
    )

    message = ft.Text(value="", color=ft.Colors.RED)

    def salvar_agendamento(e):
        if not all([date_appoint.value, time_picker.value, pet_dropdown.value, procedure_dropdown.value]):
            message.value = "Preencha todos os campos!"
            page.update()
            return

        date_time_str = f"{date_appoint.value}T{str(time_picker.value)[:5]}:00"

        payload = {
            "date_appoint": date_time_str,
            "procedure_id": int(procedure_dropdown.value),
            "pet_id": int(pet_dropdown.value),
        }

        try:
            response = requests.post(
                "http://localhost:5000/appointments",
                json=payload,
                headers={"Authorization": f"Bearer {token}"}
            )

            if response.status_code == 201:
                page.go('/appointments')
            else:
                message.value = f"Erro: {response.json().get('message', 'Erro Desconhecido')}"
                page.update()

        except Exception as err:
            message.value = f"Erro ao salvar: {err}"
            page.update()

    return ft.View(
        route="/create-appointment",
        controls=[
            ft.Column(
                [
                    ft.Text("Cadastrar Agendamento", size=30, weight="bold"),
                    date_appoint,
                    ft.Row([time_btn, time_text], alignment=ft.MainAxisAlignment.CENTER),
                    pet_dropdown,
                    procedure_dropdown,
                    message,
                    ft.ElevatedButton("Salvar", on_click=salvar_agendamento),
                    ft.TextButton("Voltar", on_click=lambda e: page.go("/appointments")),
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
