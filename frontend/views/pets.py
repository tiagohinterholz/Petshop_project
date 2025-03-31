import flet as ft
import requests
from datetime import datetime, date

def pets_view(page:ft.Page):
    token = page.session.get("access_token")
    user_id = page.session.get("user_id")
    
    create_pet_btn = ft.ElevatedButton(
        text="Cadastar Pet",
        icon = ft.icons.PETS,
        on_click=lambda e: page.go('/create-pet')
    )
    edit_pet_btn = ft.ElevatedButton(
        text="Editar Pet",
        icon=ft.icons.EDIT_ATTRIBUTES,
        on_click=lambda e: page.go('/edit-pet')
    )
    delete_pet_btn = ft.ElevatedButton(
        text="Deletar Pet",
        icon=ft.icons.DELETE,
        on_click=lambda e: page.go('/delete-pet')
    )
    create_appoint_btn = ft.ElevatedButton(
        text="Cadastar Agendamento",
        icon = ft.icons.SCHEDULE,
        on_click=lambda e: page.go('/create-appoint')
    )
    
    edit_appoint_btn = ft.ElevatedButton(
        text="Editar Agendamento",
        icon=ft.icons.HOME,
        on_click=lambda e: page.go('/edit-appoint')
    )
    delete_appoint_btn = ft.ElevatedButton(
        text="Deletar Agendamento",
        icon=ft.icons.HOME,
        on_click=lambda e: page.go('/delete-appoint')
    )
    
    voltar_button = ft.ElevatedButton(text="Voltar ao Inicio", on_click=lambda e: page.go("/dashboard"))
    
    title = ft.Text("Pets e Agendamentos", size=30, weight="bold")
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
                name = pet["name"]
                breed = pet["breed_description"]
                birth_date = pet["birth_date"]
                appoints = pet["appointments"]
                
                future_appoints = [
                    appoint for appoint in appoints
                    if datetime.strptime(appoint["date_appoint"], '%Y-%m-%d'). date() > date.today()
                ]
                future_appoints.sort(key=lambda appoint: appoint["date_appoint"])
                next_appoint = future_appoints[0] if future_appoints else None

                card = ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text(name, size=20, weight="bold"),
                                ft.Text(f"Raça: {breed}"),
                                ft.Text(f"Data de Nascimento: {birth_date}"),
                                ft.Text(
                                    f"Pŕoximo agendamento: {next_appoint['date_appoint']}"
                                    if next_appoint else "Sem agendamentos futuros"
                                ),
                                ft.Text(f"Descrição do serviço: {next_appoint['desc_appoint']}"),
                                ft.Text(f"Preço: R$ {str(next_appoint['price']).split('.')[0]},00"),
                                ft.Row(
                                    controls=[
                                        edit_pet_btn,
                                        delete_pet_btn,
                                    ]
                                )
                            ],
                            spacing=5
                        ),
                        padding=15,
                        width=400,
                        border_radius=10,
                        bgcolor=ft.colors.GREEN
                    ),
                )
                content_column.controls.append(card)
        else:
            erro.value = f"Erro ao buscar dados. Código {response.status_code}"
        
    except Exception as e:
        erro.value = f"Erro na requisição: {e}"   
    
    return ft.View(
        route="/pets",
        controls=[
            ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            create_pet_btn,
                            create_appoint_btn,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    content_column,
                    erro,
                    voltar_button,
                ],                
                scroll=ft.ScrollMode.ADAPTIVE,
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        ],
        padding=20
    )