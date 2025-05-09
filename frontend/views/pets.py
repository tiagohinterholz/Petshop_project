import flet as ft
import requests
from datetime import datetime, date

def pets_view(page:ft.Page):
    token = page.session.get("access_token")
    user_id = page.session.get("user_id")
    
    dialog = ft.AlertDialog(
        title=ft.Text(""),
        content=ft.Text(""),
        actions=[]
    )
    page.dialog = dialog
    
    def confirmar_exclusao(pet_id, nome_pet):
        dialog.title = ft.Text("Confirmação")
        dialog.content = ft.Text(f"Tem certeza que deseja excluir o pet {nome_pet}")
        
        def fechar_dialog(e):
            dialog.open = False
            page.update()
        
        def confirmar(e):
            dialog.open = False
            page.update()
            deletar_pet(pet_id)
        
        dialog.actions = [
            ft.TextButton("Cancelar", on_click=fechar_dialog),
            ft.TextButton("Sim", on_click= confirmar)
        ]
        dialog.open = True
        page.update()
    
    def deletar_pet(pet_id):
        dialog.open = False
        try:
            response = requests.delete(
                f"http://localhost:5000/pets/{pet_id}",
                headers={"Authorization": f"Bearer {token}"}
            )
            if response.status_code == 200:
                for c in content_column.controls:
                    if hasattr(c, "pet_id") and c.pet_id == pet_id:
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
    
    create_pet_btn = ft.ElevatedButton(
        text="Cadastar Pet",
        icon = ft.Icons.PETS,
        on_click=lambda e: page.go('/create-pet')
    )
    
    voltar_button = ft.ElevatedButton(text="Voltar ao Inicio", on_click=lambda e: page.go("/dashboard"))
    
    title = ft.Text("Pets", size=30, weight="bold")
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
                    if datetime.strptime(appoint["date_appoint"], "%Y-%m-%dT%H:%M:%S").date() > date.today()
                ]
                future_appoints.sort(key=lambda appoint: appoint["date_appoint"])
                next_appoint = future_appoints[0] if future_appoints else None
                procedure = next_appoint["procedure"] if next_appoint and "procedure" in next_appoint else None
             
                edit_pet_btn = ft.ElevatedButton(
                    text="Editar Pet",
                    icon=ft.Icons.EDIT_ATTRIBUTES,
                    on_click=lambda e: page.go(f"/edit-pet?id={pet['id']}")
                )
                def make_delete_button(pet_id, nome):
                    return ft.ElevatedButton(
                        text="Deletar Pet",
                        icon=ft.Icons.DELETE,
                        on_click=lambda e: confirmar_exclusao(pet_id, nome)
                    )
                delete_pet_btn = make_delete_button(pet["id"], pet["name"])
                
                card = ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text(name, size=20, weight="bold"),
                                ft.Text(f"Raça: {breed}"),
                                ft.Text(f"Data de Nascimento: {birth_date}"),
                                ft.Text(
                                    f"Pŕoximo agendamento: Data: {next_appoint['date_appoint'].split('T')[0]} | Hora: {next_appoint['date_appoint'].split('T')[1]}"
                                    if next_appoint else "Sem agendamentos futuros"
                                ),
                                ft.Text(f"Serviço Agendado: {procedure['name']}" if procedure else "-"),
                                ft.Text(f"Preço: R$ {str(procedure['price']).split('.')[0]},00" if procedure else "-"),
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
                        bgcolor=ft.Colors.GREEN_900
                    ),
                )
                card.pet_id = pet["id"]
                content_column.controls.append(card)
        else:
            erro.value = f"Erro ao buscar dados. Código {response.status_code}"
        
    except Exception as e:
        erro.value = f"Erro na requisição: {e}"   
    
    return ft.View(
        route="/pets",
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
                                create_pet_btn,
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
