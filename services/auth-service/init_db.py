# init_db.py
import os
import sys
from dotenv import load_dotenv

# Cargar variables de entorno PRIMERO
load_dotenv()

print("=" * 60)
print("🚀 INICIALIZADOR DE BASE DE DATOS - POSTGRESQL")
print("=" * 60)

try:
    # Importar después de cargar .env
    from app.core.database import engine, Base
    from app.models.user import UserDB
    
    print("📦 Creando tablas en PostgreSQL...")
    
    # Crear todas las tablas
    Base.metadata.create_all(bind=engine)
    
    print("✅ Tablas creadas exitosamente!")
    print(f"✅ Base de datos: {os.getenv('DB_NAME', 'auth_db')}")
    print(f"✅ Tabla: {UserDB.__tablename__}")
    
    # Verificar que se creó la tabla
    from sqlalchemy import inspect
    inspector = inspect(engine)
    
    if inspector.has_table("users"):
        print("✅ Verificación: Tabla 'users' existe en la base de datos")
        columns = inspector.get_columns("users")
        print(f"✅ Columnas creadas: {len(columns)}")
        for col in columns[:3]:  # Mostrar primeras 3 columnas
            print(f"   - {col['name']} ({col['type']})")
    
    print("\n" + "=" * 60)
    print("🎉 BASE DE DATOS POSTGRESQL INICIALIZADA")
    print("=" * 60)
    
    print("\n🔗 URLs útiles:")
    print(f"   PostgreSQL: postgresql://localhost:5432/{os.getenv('DB_NAME', 'auth_db')}")
    print("   API: http://localhost:3001")
    print("   Swagger UI: http://localhost:3001/docs")
    print("   Redoc: http://localhost:3001/redoc")
    
    print("\n👤 Credenciales de prueba:")
    print(f"   Usuario: {os.getenv('DB_USER', 'auth_user')}")
    print(f"   Contraseña: {os.getenv('DB_PASSWORD', 'auth_pass')}")
    print(f"   Database: {os.getenv('DB_NAME', 'auth_db')}")
    
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    print("\n📁 Verifica que tengas la estructura de carpetas:")
    print("   services/auth-service/")
    print("   ├── app/")
    print("   │   ├── core/")
    print("   │   │   └── database.py")
    print("   │   └── models/")
    print("   │       └── user.py")
    print("   ├── .env")
    print("   └── init_db.py")
    sys.exit(1)
    
except Exception as e:
    print(f"❌ Error general: {type(e).__name__}: {e}")
    print("\n🔧 Pasos para solucionar:")
    print("1. Ejecuta: docker-compose up -d")
    print("2. Espera 15 segundos: timeout 15")
    print("3. Verifica PostgreSQL: docker ps")
    print("4. Prueba conexión manual:")
    print(f'   python -c "import psycopg2; conn = psycopg2.connect(host=\'localhost\', user=\'{os.getenv("DB_USER")}\', password=\'{os.getenv("DB_PASSWORD")}\', database=\'postgres\'); print(\'✅ Conectado\')"')
    sys.exit(1)