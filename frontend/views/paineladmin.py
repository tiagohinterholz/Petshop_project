import flet as ft
import requests

def create_painel_admin_view(page: ft.Page):
    
    users_btn = ft.ElevatedButton(
                    text="Usuários",
                    icon=ft.Icons.PEOPLE,
                    on_click=lambda _: page.go("/admin/user")
                )
    clients_btn = ft.ElevatedButton(
                    text="Clientes",
                    icon=ft.Icons.PERSON_PIN,
                    on_click=lambda _: page.go("/admin/client")
                )
    addresses_btn = ft.ElevatedButton(
                    text="Endereços",
                    icon=ft.Icons.HOUSE,
                    on_click=lambda _: page.go("/admin/adress")
                )
    contacts_btn = ft.ElevatedButton(
                    text="Contatos",
                    icon=ft.Icons.CONTACT_PAGE,
                    on_click=lambda _: page.go("/admin/contact")
                )
    pets_btn = ft.ElevatedButton(
                        text="Pets",
                        icon=ft.Icons.PETS,
                        on_click=lambda _: page.go("/admin/pet")
                )
    
    appoints_btn = ft.ElevatedButton(
                        text="Agendamentos",
                        icon=ft.Icons.CALENDAR_MONTH,
                        on_click=lambda _: page.go("/admin/appoint")
                )
    
    breeds_btn = ft.ElevatedButton(
                        text="Raças",
                        icon=ft.Icons.PETS,
                        on_click=lambda _: page.go("/painel-admin")
                )
    
    procedures_btn = ft.ElevatedButton(
                        text="Procedimentos",
                        icon=ft.Icons.MEDICAL_SERVICES,
                        on_click=lambda _: page.go("/admin/procedure")
                    )
    
    voltar_button = ft.ElevatedButton(text="Voltar ao Inicio", on_click=lambda e: page.go("/dashboard"))
    
    return ft.Column(
        controls=[
            ft.Container(
                content=ft.Text("Painel Administrativo", size=24, weight="bold"),
                alignment=ft.alignment.center
            ),

            ft.Column(
                controls=[
                    ft.Row(controls=[users_btn, clients_btn], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row(controls=[addresses_btn, contacts_btn], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row(controls=[pets_btn, appoints_btn], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row(controls=[breeds_btn, procedures_btn], alignment=ft.MainAxisAlignment.CENTER),
                ],
                spacing=15,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),

            ft.Container(expand=True),  # Espaço expansível

            ft.Row(
                controls=[
                    voltar_button],
                alignment=ft.MainAxisAlignment.CENTER
            )
        ],
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,
    )
    