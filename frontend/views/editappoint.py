import flet as ft
import requests
from datetime import datetime

def edit_appointments_view(page: ft.Page):
    token = page.session.get("access_token")
    user_id = page.session.get("user_id")
    appointment_id = page.route.split("=")[-1]
    
    date_appoint = ft.TextField(label="Data do Agendamento (AAAA-MM-DD)", width=300, disabled=True)
    time_text = ft.Text(value="Horário não selecionado")
    time_picker = ft.TimePicker(
        confirm_text="OK",
        cancel_text="Cancelar",
        help_text="Selecione o horário",
        disabled=True,
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

    pet_dropdown = ft.Dropdown(label="Pet", width=300, disabled=True)
    procedure_dropdown = ft.Dropdown(label="Serviço", width=300, disabled=True)
    message = ft.Text(value="", color=ft.Colors.RED)
    
    
    cb_date_appoint = ft.Checkbox(label="Editar Data escolhida", value=False)
    cb_pet_dropdown = ft.Checkbox(label="Alterar Pet", value=False)
    cb_procedure_dropdown = ft.Checkbox(label="Alterar Procedimento", value=False)
    
    def toggle_field(field, checkbox):
        field.disabled = not checkbox.value
        page.update()

    cb_date_appoint.on_change = lambda e: toggle_field(date_appoint, cb_date_appoint)
    cb_pet_dropdown.on_change = lambda e: toggle_field(pet_dropdown, cb_pet_dropdown)
    cb_procedure_dropdown.on_change = lambda e: toggle_field(procedure_dropdown, cb_procedure_dropdown)
    
    def carregar_agendamento():
        try:
            # Carrega pets
            data_pets = requests.get(
                f"http://localhost:5000/dashboard/{user_id}",
                headers={"Authorization": f"Bearer {token}"}
            )
            pets = data_pets.json().get("pets", []) if data_pets.status_code == 200 else []
            pet_dropdown.options = [
                ft.dropdown.Option(text=pet["name"], key=str(pet["id"])) for pet in pets
            ]

            # Carrega procedimentos
            data_proc = requests.get(
                "http://localhost:5000/procedures",
                headers={"Authorization": f"Bearer {token}"}
            )
            procedures = data_proc.json() if data_proc.status_code == 200 else []
            procedure_dropdown.options = [
                ft.dropdown.Option(text=p["name"], key=str(p["id"])) for p in procedures
            ]

            # Carrega agendamento
            data_appoint = requests.get(
                f"http://localhost:5000/appointments/{appointment_id}",
                headers={"Authorization": f"Bearer {token}"}
            )
            if data_appoint.status_code == 200:
                data = data_appoint.json()
                date, hour = data["date_appoint"].split("T")
                date_appoint.value = date
                time_picker.value = datetime.strptime(hour, "%H:%M:%S").time()
                time_text.value = hour[:5]
                pet_dropdown.value = str(data["pet_id"])
                procedure_dropdown.value = str(data["procedure_id"])
            else:
                message.value = "Erro ao carregar agendamento."
        except Exception as err:
            message.value = f"Erro: {err}"
        page.update() 
    
    def salvar_agendamento(e):

        date_time_str = f"{date_appoint.value}T{time_picker.value.strftime('%H:%M')}:00"

        payload = {}
        
        if cb_date_appoint.value:
            payload['date_appoint'] = date_time_str
        if cb_procedure_dropdown.value:
            payload['procedure_id'] = int(procedure_dropdown.value)
        if cb_pet_dropdown.value:
            payload['pet_id'] = int(pet_dropdown.value)

        try:
            response = requests.put(
                f"http://localhost:5000/appointments/{appointment_id}",
                json=payload,
                headers={"Authorization": f"Bearer {token}"}
            )

            if response.status_code == 200:
                page.go("/appointments")
            else:
                message.value = f"Erro: {response.json().get('message', 'Erro Desconhecido')}"
        except Exception as err:
            message.value = f"Erro ao salvar: {err}"

        page.update()

    # Chama carregamento inicial
    carregar_agendamento()

    return ft.View(
        route="/edit-appointment",
        controls=[
            ft.Column(
                controls=[
                    ft.Text("Editar Agendamento", size=30, weight="bold"),
                    cb_date_appoint,
                    date_appoint,
                    ft.Row([time_btn, time_text], alignment=ft.MainAxisAlignment.CENTER),
                    cb_pet_dropdown,   
                    pet_dropdown,
                    cb_procedure_dropdown,
                    procedure_dropdown,
                    message,
                    ft.ElevatedButton("Salvar Alterações", on_click=salvar_agendamento),
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
    
