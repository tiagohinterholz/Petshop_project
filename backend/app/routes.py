from flask import Blueprint

main = Blueprint('main', __name__)

@main.route("/")
def home():
    return "API do Petshop rodando com Flask"