import flet as ft
import requests


def profile_view(page: ft.Page):
    token = page.session.get("access_token")
    user_id = page.session.get("user_id")
    
    contact = None
    address = None
    client = None
    register_client_btn = None
    
    dialog = ft.AlertDialog(
        title=ft.Text(""),
        content=ft.Text(""),
        actions=[
            ft.TextButton("OK", on_click=lambda e: close_dialog())
        ]
    )
    page.dialog = dialog
    
    def open_dialog(title, content):
        dialog.title = ft.Text(title)
        dialog.content = ft.Text(content)
        dialog.open = True
        page.update()
        
    def close_dialog():
        dialog.open = False
        page.update()
            
    edit_address_btn = ft.ElevatedButton(
        text="Editar Endereço",
        icon=ft.Icons.HOME,
        on_click=lambda e: page.go("/edit-address"),
    )
    create_address_btn = ft.ElevatedButton(
        text="Cadastrar Endereço",
        icon=ft.Icons.HOME,
        on_click=lambda e: page.go("/create-address"),
    )
    edit_contact_btn = ft.ElevatedButton(
        text="Editar Contato",
        icon=ft.Icons.CONTACT_PHONE,
        on_click=lambda e: page.go("/edit-contact"),
    )
    create_contact_btn = ft.ElevatedButton(
        text="Cadastrar Contato",
        icon=ft.Icons.CONTACT_PHONE,
        on_click=lambda e: page.go("/create-contact"),
    )

    title = ft.Text("Perfil do Usuário", size=30, weight="bold")
    dados_contato = ft.Text()
    dados_endereco = ft.Text()
    erro = ft.Text(color=ft.Colors.RED)

    try:
        response = requests.get(
            f"http://localhost:5000/dashboard/{user_id}",
            headers={"Authorization": f"Bearer {token}"}
        )

        if response.status_code == 200:
            data = response.json()
            client = data.get("client") or {}
            contact = data.get("contact")
            address = data.get("address")
            
            if not client:
                def registrar_client(e):
                    try:
                        response = requests.post(
                            f"http://localhost:5000/clients",
                            json={
                                "user_id": user_id,
                                },
                            headers={"Authorization": f"Bearer {token}"}
                        )
                        if response.status_code == 201:
                            register_client_btn.visible = False
                            open_dialog("Sucesso", "Cliente registrado com sucesso")
                        else:
                            open_dialog("Erro", f"Falha ao registrar cliente. Código: {response.status_code}")    
                    except Exception as err:
                        open_dialog("Erro", f"Erro na requisição: {err}")
                    
                register_client_btn = ft.ElevatedButton(
                    text="Registrar Cliente",
                    icon=ft.Icons.PERSON_ADD,
                    on_click=registrar_client
                )
                                  
            nome = client.get("name", "N/A")
            
            value_contact = contact.get("value_contact", "N/A")
            type_contact = contact.get("type_contact", "N/A")
            
            rua = address.get("street", "N/A")
            cidade = address.get("city", "N/A")
            bairro = address.get("neighborhood", "N/A")
            complemento = address.get("complement", "N/A")
            
            dados_contato.value = f"Nome: {nome}\nContato: {value_contact}\nTipo de Contato: {type_contact}"
            dados_endereco.value = f"Endereço: Rua {rua}, número: {complemento}\nBairro: {bairro}\nCidade: {cidade}"
        else:
            erro.value = f"Erro ao buscar dados. Código {response.status_code}"

    except Exception as e:
        erro.value = f"Erro na requisição: {e}"

    voltar_button = ft.ElevatedButton(text="Voltar ao Inicio", on_click=lambda e: page.go("/dashboard"))  
    
    return ft.View(
    route="/profile",
    controls=[
        dialog,
        ft.Container(
            content=ft.Column(
                controls=[
                    title,

                    ft.Row(
                        controls=[
                            # Coluna de Contato
                            ft.Column(
                                controls=[
                                    dados_contato,
                                    edit_contact_btn if contact and "value_contact" in contact else create_contact_btn,
                                ],
                                spacing=10,
                                expand=True
                            ),
                            ft.VerticalDivider(width=1),
                            # Coluna de Endereço
                            ft.Column(
                                controls=[
                                    dados_endereco,
                                    edit_address_btn if address and "street" in address else create_address_btn,
                                ],
                                spacing=10,
                                expand=True
                            )
                        ],
                        spacing=20,
                        expand=True
                    ),

                    erro,

                    ft.Container(
                        padding=10,
                        alignment=ft.alignment.center,
                        content=ft.Row(
                            controls=[voltar_button, register_client_btn] if register_client_btn else [voltar_button],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=20
                        )
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
            ),
            alignment=ft.alignment.center,
            expand=True
        )
    ],
    padding=20
)