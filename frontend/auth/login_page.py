import flet as ft
import requests
import jwt

def login_view(page: ft.Page):
    
    cpf_input = ft.TextField(label="CPF", 
                             autofocus=True, 
                             hint_text="000.000.000-00",
                             on_change=lambda e: formatar_cpf(e))
    
    password_input=ft.TextField(label="Senha", password=True, can_reveal_password=True)
    error_text = ft.Text(value="", color=ft.colors.RED)
    
    def formatar_cpf(e):
        texto = cpf_input.value
        so_numeros = ''.join(filter(str.isdigit, texto))[:11]
        
        if len(so_numeros) <= 3:
            formatado = so_numeros
        elif len(so_numeros) <= 6:
            formatado = f"{so_numeros[:3]}.{so_numeros[3:]}"
        elif len(so_numeros) <= 9:
            formatado = f"{so_numeros[:3]}.{so_numeros[3:6]}.{so_numeros[6:]}"
        else:
            formatado = f"{so_numeros[:3]}.{so_numeros[3:6]}.{so_numeros[6:9]}-{so_numeros[9:]}"

        cpf_input.value = formatado
        page.update()
            
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
                token = response.json().get("access_token")
                refresh_token = response.json().get("refresh_token")
                payload = jwt.decode(token, options={"verify_signature": False}, algorithms=["HS256"])
                cpf = payload.get("sub")
                page.session.set("token", token)
                page.session.set("cpf", cpf)
                page.session.set("refresh", refresh_token)
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