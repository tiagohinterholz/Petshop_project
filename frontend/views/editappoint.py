import flet as ft
import requests

def edit_appointments_view(page: ft.Page):
    token = page.session.get("access_token")
    user_id = page.session.get("user_id")