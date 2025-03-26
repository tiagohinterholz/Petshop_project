import flet as ft
import requests

def dashboard_view(page: ft.Page):
    token = page.session.get("token")
    get_cpf = page.session.get("cpf")
     
    saudacao = ft.Text("Bem- vindo", size=25, weight="bold")
    perfil = ft.Text()
    dados_usuario = ft.Text()
    
    try:
        response = requests.get(
            f"http://localhost:5000/users/{get_cpf}",
            headers={"authorization": f"Bearer {token}"}
        )
        if response.status_code == 200:
            data = response.json()
            nome = data.get("name")
            email = data.get("email"),
            role = "Administrador" if data.get("is_admin") else "Cliente"

            saudacao.value = f"Bem-vindo, {nome}"
            perfil.value = ""
            dados_usuario.value = f"Perfil Logado: {role}"
            
            
    except Exception as err:
        saudacao.value = "Erro de conexão."
        dados_usuario.value = str(err)
    
    lista_pets = ft.Text("Pets Cadastrados...")
    lista_agendamentos = ft.Text("Agendamentos Cadastrados...")
    
    layout = ft.Column(
        controls=[
            saudacao,
            perfil,
            ft.Divider(),
            dados_usuario,
            ft.Divider(),
            lista_pets,
            ft.Divider(),
            lista_agendamentos
        ],
        scroll=ft.ScrollMode.ADAPTIVE,
        spacing=20
    )
    
    return ft.View(
        route="/",
        controls=[layout],
        padding=20
    )