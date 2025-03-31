import flet as ft
import requests


def profile_view(page: ft.Page):
    token = page.session.get("access_token")
    user_id = page.session.get("user_id")
    
            
    edit_address_btn = ft.ElevatedButton(
        text="Editar Endereço",
        icon=ft.icons.HOME,
        on_click=lambda e: page.go("/edit-address"),
    )
    
    create_address_btn = ft.ElevatedButton(
        text="Cadastrar Endereço",
        icon=ft.icons.HOME,
        on_click=lambda e: page.go("/create-address"),
    )

    edit_contact_btn = ft.ElevatedButton(
        text="Editar Contato",
        icon=ft.icons.CONTACT_PHONE,
        on_click=lambda e: page.go("/edit-contact"),
    )
    
    create_contact_btn = ft.ElevatedButton(
        text="Cadastrar Contato",
        icon=ft.icons.CONTACT_PHONE,
        on_click=lambda e: page.go("/create-contact"),
    )

    title = ft.Text("Perfil do Usuário", size=30, weight="bold")
    dados = ft.Text()
    erro = ft.Text(color=ft.Colors.RED)

    try:
        response = requests.get(
            f"http://localhost:5000/dashboard/{user_id}",
            headers={"Authorization": f"Bearer {token}"}
        )

        if response.status_code == 200:
            data = response.json()
            client = data.get("client") or {}
            contact = data.get("contact") or {}
            address = data.get("address") or {}
            
            buttons = []

            if address:
                buttons.append(ft.ElevatedButton("Editar Endereço", on_click=lambda e: page.go("/edit-address")))
            else:
                buttons.append(ft.ElevatedButton("Cadastrar Endereço", on_click=lambda e: page.go("/address")))
                
            if contact:
                buttons.append(ft.ElevatedButton("Editar Contato", on_click=lambda e: page.go("/edit-contact")))
            else:
                buttons.append(ft.ElevatedButton("Cadastrar Contato", on_click=lambda e: page.go("/create-address")))
                        
            nome = client.get("name", "N/A")
            email = contact.get("value_contact", "N/A")
            rua = address.get("street")
            cidade = address.get("city")
            bairro = address.get("neighborhood")
            complemento = address.get("complement")

            dados.value = f"Nome: {nome}\nContato: {email}\nEndereço: Rua {rua}, número: {complemento}\nBairro: {bairro}\nCidade: {cidade}"
        else:
            erro.value = f"Erro ao buscar dados. Código {response.status_code}"

    except Exception as e:
        erro.value = f"Erro na requisição: {e}"

    voltar_button = ft.ElevatedButton(text="Voltar ao Inicio", on_click=lambda e: page.go("/dashboard"))  
    
    return ft.View(
        route="/profile",
        controls=[
            ft.Container(
                content=ft.Column(
                    controls=[
                        title,
                        dados,
                        ft.Row(
                            controls=[*buttons],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        erro,
                        voltar_button
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20
                ),
                alignment=ft.alignment.center
            )
        ],
        padding=20
    )