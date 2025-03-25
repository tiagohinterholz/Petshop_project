import flet as ft

def main(page:ft.Page):
    
    # Detecta quando a rota muda
    def route_change(e: ft.RouteChangeEvent):
        page.views.clear() # limpa as views atuais
        
        if page.route == "/login":
            page.views.append(
                ft.View(
                    route="/login",
                    controls=[
                        ft.Text("Tela de Login (Temporária)")
                    ],
                )
            )
        elif page.route == "/":
            page.views.append(
                ft.View(
                    route="/",
                    controls=[
                        ft.Text("Dashboard (temporário)")
                    ],
                )
            )
            
        page.update()    
        
    page.on_route_change = route_change
    page.go("/login")
        
ft.app(target=main)