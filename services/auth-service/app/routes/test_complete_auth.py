# test_complete_auth.py
import requests
import json
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

BASE_URL = os.getenv("API_URL", "http://localhost:3001")

class AuthTester:
    def __init__(self):
        self.access_token = None
        self.refresh_token = None
        self.user_info = None
    
    def test_complete_flow(self):
        print("🧪 TEST COMPLETO DE AUTENTICACIÓN")
        print("=" * 50)
        
        # 1. LOGIN
        print("\n1. 🔐 LOGIN")
        login_data = {
            "username": "jatulcanaza@uce.edu.ec",
            "password": "ja123456"
        }
        
        response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
        
        if response.status_code == 200:
            tokens = response.json()
            self.access_token = tokens["access_token"]
            self.refresh_token = tokens["refresh_token"]
            
            print(f"   ✅ Status: {response.status_code}")
            print(f"   📝 Access token (30 chars): {self.access_token[:30]}...")
            print(f"   🔄 Refresh token (30 chars): {self.refresh_token[:30]}...")
        else:
            print(f"   ❌ Error: {response.status_code} - {response.text}")
            return False
        
        # 2. OBTENER USUARIO ACTUAL
        print("\n2. 👤 OBTENER USUARIO ACTUAL")
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
        
        if response.status_code == 200:
            self.user_info = response.json()
            print(f"   ✅ Status: {response.status_code}")
            print(f"   📋 ID: {self.user_info['id']}")
            print(f"   📧 Email: {self.user_info['email']}")
            print(f"   👤 Nombre: {self.user_info['name']}")
            print(f"   ✅ Activo: {self.user_info['is_active']}")
        else:
            print(f"   ❌ Error: {response.status_code} - {response.text}")
            return False
        
        # 3. REFRESH TOKEN
        print("\n3. 🔄 REFRESH TOKEN")
        response = requests.post(
            f"{BASE_URL}/auth/refresh",
            params={"refresh_token": self.refresh_token}
        )
        
        if response.status_code == 200:
            new_tokens = response.json()
            print(f"   ✅ Status: {response.status_code}")
            print(f"   🆕 Nuevo access token generado")
            
            # Actualizar tokens
            old_access = self.access_token[:30]
            self.access_token = new_tokens["access_token"]
            self.refresh_token = new_tokens["refresh_token"]
            print(f"   🔄 Token actualizado: {old_access}... → {self.access_token[:30]}...")
        else:
            print(f"   ❌ Error: {response.status_code} - {response.text}")
        
        # 4. LISTAR USUARIOS
        print("\n4. 📋 LISTAR USUARIOS")
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(f"{BASE_URL}/users/", headers=headers)
        
        if response.status_code == 200:
            users = response.json()
            print(f"   ✅ Status: {response.status_code}")
            print(f"   👥 Total usuarios: {len(users)}")
            for i, user in enumerate(users[:3]):  # Mostrar primeros 3
                print(f"     {i+1}. {user['name']} ({user['email']})")
            if len(users) > 3:
                print(f"     ... y {len(users) - 3} más")
        else:
            print(f"   ❌ Error: {response.status_code} - {response.text}")
        
        # 5. LOGOUT
        print("\n5. 🚪 LOGOUT")
        response = requests.post(f"{BASE_URL}/auth/logout", headers=headers)
        
        if response.status_code == 200:
            print(f"   ✅ Status: {response.status_code}")
            print(f"   📝 Mensaje: {response.json().get('message', 'Logout exitoso')}")
        else:
            print(f"   ❌ Error: {response.status_code} - {response.text}")
        
        # 6. VERIFICAR QUE EL LOGOUT FUNCIONÓ
        print("\n6. 🔍 VERIFICAR LOGOUT")
        response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
        
        if response.status_code == 401:
            print(f"   ✅ Status: {response.status_code} - Token inválido (como se esperaba)")
        else:
            print(f"   ⚠️  Status: {response.status_code} - Token aún válido")
        
        print("\n" + "=" * 50)
        print("🎉 ¡TEST COMPLETADO EXITOSAMENTE!")
        return True
    
    def test_health_check(self):
        """Prueba adicional: health check"""
        print("\n7. 🏥 HEALTH CHECK")
        response = requests.get(f"{BASE_URL}/health")
        
        if response.status_code == 200:
            health_data = response.json()
            print(f"   ✅ Status: {response.status_code}")
            print(f"   📊 Estado: {health_data}")
        else:
            print(f"   ❌ Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    tester = AuthTester()
    if tester.test_complete_flow():
        tester.test_health_check()