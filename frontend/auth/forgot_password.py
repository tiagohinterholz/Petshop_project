import flet as ft
import requests

def forgot_password_view(page: ft.Page):
    email_input = ft.TextField(label="E-mail", autofocus=True)
    feedback_text = ft.Text(value="", color=ft.colors.GREEN)
    
    def enviar_link(e):
        email = email_input.value
        if not email:
            feedback_text.value = "Informe seu e-mail:"
            feedback_text.color = ft.colors.RED
            page.update()
            return
        
        try:
            response = requests.post(
                "http://localhost:5000/forgot-password",
                json={"email": email}
            )
            if response.status_code == 200:
                feedback_text.value = "Link de recuperação enviado!"
                feedback_text.color = ft.colors.GREEN
            else:
                feedback_text.value = "E-mail não encontrado."
                feedback_text.color = ft.colors.RED
        
        except Exception as err:
            feedback_text.value = f"Erro: {err}"
            feedback_text.color = ft.colors.RED
        
        page.update()
    
    return ft.View(
        route="/forgot-password",
        controls=[
            ft.Column(
                controls=[
                    ft.Text("Recuperar senha", size=25, weight="bold"),
                    email_input,
                    feedback_text,
                    ft.ElevatedButton("Enviar link", on_click=enviar_link),
                    ft.TextButton("Voltar para login", on_click=lambda e: page.go("/login"))
                ],
                width=300,
                spacing=20,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )