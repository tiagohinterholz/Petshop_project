import flet as ft

def build_sidebar(page: ft.Page, profile):
    
    dash_btn = ft.ListTile(
                    title=ft.Text("Dashboard"),
                    leading=ft.Icon(ft.Icons.HOME),
                    on_click=lambda _: page.go("/dashboard")
                )
    pets_btn = ft.ListTile(
                    title=ft.Text("Pets"),
                    leading=ft.Icon(ft.Icons.PETS),
                    on_click=lambda _: page.go("/pets")
                )
    appoints_btn = ft.ListTile(
                    title=ft.Text("Agendamentos"),
                    leading=ft.Icon(ft.Icons.CALENDAR_MONTH),
                    on_click=lambda _: page.go("/appointments")
                )
    profile_btn = ft.ListTile(
                    title=ft.Text("Perfil"),
                    leading=ft.Icon(ft.Icons.PERSON),
                    on_click=lambda _: page.go("/profile")
                )
    painel_adm_btn = ft.ListTile(
                        title=ft.Text("Painel do Administrador"),
                        leading=ft.Icon(ft.Icons.ADMIN_PANEL_SETTINGS),
                        on_click=lambda _: page.go("/painel-admin")
                    )
    
    return ft.Column(
        controls=[
            ft.Text("Menu", size=18, weight="bold"),
            ft.Divider(),
            dash_btn,
            pets_btn,
            appoints_btn,
            profile_btn,
            *([painel_adm_btn] if profile == 'Administrador' else [])
                        
        ],
        width=200,
        spacing=5,
        expand=5
    )