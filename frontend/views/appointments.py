import flet as ft
import requests
from datetime import datetime, date

def appointments_view(page:ft.Page):
    token = page.session.get("access_token")
    user_id = page.session.get("user_id")
    
    dialog = ft.AlertDialog(
        title=ft.Text(""),
        content=ft.Text(""),
        actions=[]
    )
    page.dialog = dialog
    
    def confirmar_exclusao(appointment_id, nome_appoint):
        dialog.title = ft.Text("Confirmação")
        dialog.content = ft.Text(f"Tem certeza que deseja excluir o pet {nome_appoint}")
        
        def fechar_dialog(e):
            dialog.open = False
            page.update()
        
        def confirmar(e):
            dialog.open = False
            page.update()
            deletar_appointment(appointment_id)
        
        dialog.actions = [
            ft.TextButton("Cancelar", on_click=fechar_dialog),
            ft.TextButton("Sim", on_click= confirmar)
        ]
        dialog.open = True
        page.update()
    
    def deletar_appointment(appointment_id):
        dialog.open = False
        try:
            response = requests.delete(
                f"http://localhost:5000/appointments/{appointment_id}",
                headers={"Authorization": f"Bearer {token}"}
            )
            if response.status_code == 200:
                for c in content_column.controls:
                    if hasattr(c, "appointment_id") and c.pet.appointment_id == appointment_id:
                        content_column.controls.remove(c)
                        break
                page.update()
            else:
                data = response.json()
                erro.value = f"{data.get('error', 'Erro desconhecido')}"
                page.update()
        except Exception as e:
            erro.value = f"Erro na exclusão: {e}"
            page.update()
    
    create_appoint_btn = ft.ElevatedButton(
        text="Cadastar Agendamento",
        icon = ft.Icons.SCHEDULE,
        on_click=lambda e: page.go('/create-appointment')
    )
    
    voltar_button = ft.ElevatedButton(text="Voltar ao Inicio", on_click=lambda e: page.go("/dashboard"))
    
    title = ft.Text("Agendamentos", size=30, weight="bold")
    content_column= ft.Column(spacing=10)
    erro = ft.Text(color=ft.Colors.RED)
    
    try:
        response = requests.get(
            f"http://localhost:5000/dashboard/{user_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        if response.status_code == 200:
            data = response.json()
            pets= data.get("pets" or [])
            
            for pet in pets:
                pet_name = pet["name"]

                for appoint in pet["appointments"]:
                    
                    dt = datetime.strptime(appoint["date_appoint"], "%Y-%m-%dT%H:%M:%S")
                    data_formatada = dt.strftime("%d/%m/%Y")
                    hora_formatada = dt.strftime("%H:%M")
                    
                    # Filtro de futuros
                    if datetime.strptime(appoint["date_appoint"], "%Y-%m-%dT%H:%M:%S").date() > date.today():
                        procedure = appoint.get("procedure")
                        appoint_id = appoint.get("id")

                        edit_appoint_btn = ft.ElevatedButton(
                            text="Editar",
                            icon=ft.Icons.EDIT,
                            on_click=lambda e, id=appoint_id: page.go(f"/edit-appoint?id={id}")
                        )

                        delete_appoint_btn = ft.ElevatedButton(
                            text="Excluir",
                            icon=ft.Icons.DELETE,
                            on_click=lambda e, id=appoint_id: confirmar_exclusao(id, procedure["description"])
                        )

                        card = ft.Card(
                            content=ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Text(procedure["name"], size=20, weight="bold"),
                                        ft.Text(f"Descrição: {procedure.get('description', '-')}" if procedure else "-"),
                                        ft.Text(f"Preço: R$ {str(procedure['price']).split('.')[0]},00" if procedure else "-"),
                                        ft.Text(f"Pet: {pet_name}"),
                                        ft.Text(f"Data: {data_formatada}"),
                                        ft.Text(f"Hora: {hora_formatada}"),
                                        ft.Row(
                                            controls=[edit_appoint_btn, delete_appoint_btn],
                                            alignment=ft.MainAxisAlignment.END
                                        )
                                    ],
                                    spacing=5
                                ),
                                padding=15,
                                width=400,
                                border_radius=10,
                                bgcolor=ft.Colors.GREEN_900
                            )
                        )
                        card.appointment_id = appoint_id
                        content_column.controls.append(card)
        else:
            erro.value = f"Erro ao buscar dados. Código {response.status_code}"
        
    except Exception as e:
        erro.value = f"Erro na requisição: {e}"   
    
    return ft.View(
        route="/appointments",
        controls=[
            dialog,
            ft.Column(
                controls=[
                    ft.Column(
                        controls=[
                            content_column,
                            erro,
                        ],
                        scroll=ft.ScrollMode.ADAPTIVE,
                        expand=True
                    ),
                    ft.Container(  # Footer fixo com botões
                        padding=10,
                        alignment=ft.alignment.center,
                        content=ft.Row(
                            controls=[
                                voltar_button,
                                create_appoint_btn,
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=20
                        )
                    )
                ],
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        ],
        padding=20
    )