import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

try:
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    cursor.execute("SELECT version();")
    db_version = cursor.fetchone()
    
    print(f"✅ Conexão bem-sucedida! PostgreSQL versão: {db_version[0]}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"Erro ao conectar ao banco de dados: {e}")