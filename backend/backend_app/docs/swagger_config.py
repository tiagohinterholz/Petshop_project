swagger_config = {
    "swagger": "2.0",
    "info": {
        "title": "API do Petshop",
        "description": "Documentação da API para gerenciamento do petshop",
        "version": "1.0.0",
        "contact": {
            "name": "Tiago F. Hinterholz",
            "email": "fh.tiago@gmail.com",
        }
    },
    "host": "127.0.0.1:5000",
    "basePath": "/",
    "schemes": ["http"],
    "tags": [
        {
            "name": "Address",
            "description": "Endpoints relacionados ao endereço do usuário."
        }  
    ],
    "specs": [
        {
            "endpoint": "apispec_1",
            "route": "/apispec_1.json",
            "rule_filter": lambda rule: True,  # Filtra todas as rotas para documentação
            "model_filter": lambda tag: True  # Inclui todos os modelos
        }
    ],
    "static_url_path": "/flasgger_static",  # Necessário para os assets do Swagger UI
    "swagger_ui": True,  # Ativa o Swagger UI
    "specs_route": "/apidocs/",  # Define a URL da documentação
    "headers": []
}   