import flet as ft
import requests
from components.header import build_header
from components.sidebar import build_sidebar

def dashboard_view(page: ft.Page):
    token = page.session.get("access_token")
    user_id = page.session.get("user_id")
       
    saudacao = ft.Text("Bem- vindo", size=20, weight="bold")
    dados_usuario = ft.Text()
    lista_agendamentos_view = ft.Text()
    
    try:
        response = requests.get(
            f"http://localhost:5000/dashboard/{user_id}",
            headers={"authorization": f"Bearer {token}"}
        )
        if response.status_code == 200:
            pets_text = ""
            data = response.json()
            client = data.get("client") or {}
            pets = data.get("pets") or []
                        
            nome = client.get("name")
            role = "Administrador" if page.session.get("profile") == 'admin' else "Cliente"
            
            saudacao.value = f"Bem-vindo, {nome}"
            dados_usuario.value = f"Perfil: {role}"
            
            agendamentos_text = ""
            
            for pet in pets:
                nome_pet = pet.get("name", "Sem nome")
                description = pet.get("breed_description")
                pets_text += f"{nome_pet} - Raça: {description}\n"

                for a in pet.get("appointments", []):
                    agendamentos_text += f"Agendamento: {a.get('desc_appoint')} - Data de atendimento:{a.get('date_appoint')}\n"
            
            lista_agendamentos_view.value = agendamentos_text or "Nenhum agendamento cadastrado" 
        else:
            saudacao.value = "Erro ao carregar dados do usuário."
            dados_usuario.value = f"Status: {response.status_code}"
           
    except Exception as err:
        saudacao.value = "Erro de conexão."
        dados_usuario.value = str(err)
        
    conteudo_principal = ft.Column(
        controls=[
            saudacao,
            ft.Divider(),
            
            ft.Container(
                bgcolor=ft.Colors.GREY_100,
                border_radius=10,
                padding=10,
                content=ft.Text(dados_usuario.value)
            ),
            
            ft.Divider(),
            
            ft.Text("Agendamentos Futuros", size=20, weight="bold"),
            ft.Container(
                bgcolor=ft.Colors.GREY_200,
                border_radius=10,
                padding=10,
                content=ft.Text(lista_agendamentos_view.value)
            ),
            
            ft.Divider(),
            
            ft.Text("Calendário", size=20, weight="bold"),
            ft.Container(
                bgcolor=ft.Colors.GREEN_900,
                border_radius=10,
                height=200,
                alignment=ft.alignment.center,
                content=ft.Text("📅 Aqui vai o calendário futuramente", italic=True)
            ),
        ],
        scroll=ft.ScrollMode.ADAPTIVE,
        expand=True,
        spacing=10
    )
    
    layout = ft.Column(
        controls=[
            build_header(page),
            ft.Row(
                controls=[
                build_sidebar(page),
                ft.VerticalDivider(width=1),
                conteudo_principal
                ],
                expand=True,
                vertical_alignment=ft.CrossAxisAlignment.START
            )
        ],
        expand=True
    )
    
    return ft.View(
        route="/dashboard",
        controls=[layout],
        padding=20
    )