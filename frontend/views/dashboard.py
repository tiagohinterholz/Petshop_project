import flet as ft
import requests

def dashboard_view(page: ft.Page):
    token = page.session.get("access_token")
    user_id = page.session.get("user_id")
     
    saudacao = ft.Text("Bem- vindo", size=20, weight="bold")
    perfil = ft.Text()
    dados_usuario = ft.Text()
    lista_pets_view = ft.Text()
    lista_agendamentos_view = ft.Text()
    
    try:
        response = requests.get(
            f"http://localhost:5000/dashboard/{user_id}",
            headers={"authorization": f"Bearer {token}"}
        )
        if response.status_code == 200:
            data = response.json()
            client = data.get("client") or {}
            contact = data.get("contact") or {}
            pets = data.get("pets") or []
                        
            nome = client.get("name")
            role = "Administrador" if page.session.get("profile") == 'admin' else "Cliente"
            email = contact.get("value_contact", "N/A")
            
            saudacao.value = f"Bem-vindo, {nome}"
            dados_usuario.value = f"Perfil: {role} | Contato: {email}"
            
            pets_text = ""
            agendamentos_text = ""
            
            for pet in pets:
                nome_pet = pet.get("name", "Sem nome")
                breed_id = pet.get("breed_id")
                pets_text += f"{nome_pet} - Raça ID: {breed_id}\n"

                for a in pet.get("appointments", []):
                    agendamentos_text += f"{a.get('desc_appoint')} - {a.get('date_appoint')}\n"
            
            lista_pets_view.value = pets_text or "Nenhum pet cadastrado."
            lista_agendamentos_view.value = agendamentos_text or "Nenhum agendamento cadastrado" 
        else:
            saudacao.value = "Erro ao carregar dados do usuário."
            dados_usuario.value = f"Status: {response.status_code}"
           
    except Exception as err:
        saudacao.value = "Erro de conexão."
        dados_usuario.value = str(err)
        
    layout = ft.Column(
        controls=[
            saudacao,
            perfil,
            ft.Divider(),
            dados_usuario,
            ft.Divider(),
            ft.Row(
                controls=[
                    ft.Container(
                        content=lista_pets_view,
                        expand=True,
                    ),
                    ft.Container(
                        content=lista_agendamentos_view,
                        expand=True,
                    )
                ]
            )
        ],
        scroll=ft.ScrollMode.ADAPTIVE,
        spacing=5
    )
    
    return ft.View(
        route="/",
        controls=[layout],
        padding=20
    )