import flet as ft
import requests

def login_view(page: ft.Page):
    
    cpf_input = ft.TextField(label="CPF", autofocus=True, hint_text="000.000.000-00")
    password_input=ft.TextField(label="Senha", password=True, can_reveal_password=True)
    error_text = ft.Text(value="", color=ft.colors.RED)
        
    def efetuar_login(e):
        cpf = cpf_input.value
        senha = password_input.value
        
        if not cpf or not senha:
            error_text.value = "Preencha e-mail e senha"
            page.update()
        
        try:
            response = requests.post(
                "http://localhost:5000/login",
                json={"cpf": cpf, "password": senha}
            )
            
            if response.status_code == 200:
                token = response.json().get("access")
                page.session.set("token", token)
                page.go("/")
            else:
                error_text.value = "Credenciais inválidas."
                page.update()
        
        except Exception as err:
            error_text.value = f"Erro na conexão: {err}"
            page.update()
    
    login_button = ft.ElevatedButton(text="Entrar", on_click=efetuar_login)
    forgot_pass_button = ft.TextButton(text="Recuperar senha", on_click=lambda e: page.go("/forgot-password"))
    
    return ft.View(
        route="/login",
        controls=[
            ft.Column(
                controls=[
                    ft.Text("Login", size=30, weight="bold"),
                    cpf_input,
                    password_input,
                    error_text,
                    login_button,
                    forgot_pass_button
                ],
                width=300,
                spacing=20,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
            
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )