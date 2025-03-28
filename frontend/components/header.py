import flet as ft

def build_header(page: ft.Page):
    return ft.Container(
        bgcolor=ft.colors.BLUE_100,
        padding=ft.padding.symmetric(horizontal=20),
        content=ft.Row(
            controls=[
                ft.Text("Petshop App", size=25, weight="bold"),
                ft.IconButton(
                    icon=ft.icons.EXIT_TO_APP,
                    tooltip="Sair",
                    on_click=lambda _: page.go("/login")
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            height=60,          
        )
    )
        