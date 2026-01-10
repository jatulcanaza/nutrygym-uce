import psycopg
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

print("🔄 Intentando conectar a PostgreSQL...")

conn = psycopg.connect(
    host=os.getenv("DB_HOST", "localhost"),
    port=int(os.getenv("DB_PORT", 5432)),
    dbname=os.getenv("DB_NAME", "auth_db"),
    user=os.getenv("DB_USER", "auth_user"),
    password=os.getenv("DB_PASSWORD", "auth_pass"),
    options="-c client_encoding=UTF8"
)

print("✅ CONEXIÓN PYTHON OK")
conn.close()

