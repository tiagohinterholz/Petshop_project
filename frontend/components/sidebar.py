import flet as ft

def build_sidebar(page: ft.Page):
    return ft.Column(
        controls=[
            ft.Text("Menu", size=18, weight="bold"),
            ft.Divider(),
            ft.ListTile(
                title=ft.Text("Dashboard"),
                leading=ft.Icon(ft.Icons.HOME),
                on_click=lambda _: page.go("/dashboard")
            ),
            ft.ListTile(
                title=ft.Text("Pets"),
                leading=ft.Icon(ft.Icons.PETS),
                on_click=lambda _: page.go("/pets")
            ),
            ft.ListTile(
                title=ft.Text("Agendamentos"),
                leading=ft.Icon(ft.Icons.CALENDAR_MONTH),
                on_click=lambda _: page.go("/appointments")
            ),
            ft.ListTile(
                title=ft.Text("Perfil"),
                leading=ft.Icon(ft.Icons.PERSON),
                on_click=lambda _: page.go("/profile")
            ),
        ],
        width=200,
        spacing=5,
        expand=5
    )