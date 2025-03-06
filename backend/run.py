from backend_app import create_app

app = create_app()  # Cria a aplicação corretamente

if __name__ == '__main__':
    app.run(debug=True)
