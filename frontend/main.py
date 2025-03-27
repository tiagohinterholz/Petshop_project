import flet as ft
from auth.login_page import login_view
from auth.forgot_password import forgot_password_view
from views.dashboard import dashboard_view

def main(page:ft.Page):
    
    # Detecta quando a rota muda
    def route_change(e: ft.RouteChangeEvent):
        page.views.clear() # limpa as views atuais
        
        if page.route == "/login":
            page.views.append(login_view(page))
        
        elif page.route == "/forgot-password":
            page.views.append(forgot_password_view(page))
        
        elif page.route == "/dashboard":
            page.views.append(dashboard_view(page))
            
        page.update()    
        
    page.on_route_change = route_change
    page.go("/login")
        
ft.app(target=main)