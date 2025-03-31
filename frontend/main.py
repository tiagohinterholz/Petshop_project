import flet as ft
from auth.login_page import login_view
from auth.forgot_password import forgot_password_view
from views.dashboard import dashboard_view
from views.profile import profile_view
from views.createaddress import create_address_view
from views.createcontact import create_contact_view
from views.editaddress import edit_address_view
from views.editcontact import edit_contact_view
from views.pets import pets_view
from views.createpet import create_pet_view
from views.editpet import edit_pet_view
from views.createbreed import create_breed_view

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
        
        elif page.route == "/profile":
            page.views.append(profile_view(page))
            
        elif page.route == "/create-address":
            page.views.append(create_address_view(page))
        
        elif page.route == "/create-contact":
            page.views.append(create_contact_view(page))
        
        elif page.route == "/edit-address":
            page.views.append(edit_address_view(page))
        
        elif page.route == "/edit-contact":
            page.views.append(edit_contact_view(page))
            
        elif page.route == "/pets":
            page.views.append(pets_view(page))
            
        elif page.route == "/create-pet":
            page.views.append(create_pet_view(page))
        
        elif page.route == "/create-breed":
            page.views.append(create_breed_view(page))
        
        elif page.route.startswith("/edit-pet"):
            page.views.append(edit_pet_view(page))
                    
        page.update()    
        
    page.on_route_change = route_change
    page.go("/login")
        
ft.app(target=main)