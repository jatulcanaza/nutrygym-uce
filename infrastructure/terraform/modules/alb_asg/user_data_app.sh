#!/bin/bash
set -eo pipefail

exec > >(tee -a /var/log/nutrygym-app-bootstrap.log) 2>&1
echo "[APP] $(date) Starting NutryGym APP bootstrap..."

APP_DIR="/opt/nutrygym"
mkdir -p "$${APP_DIR}"
cd "$${APP_DIR}"

if [ -f /opt/nutrygym/app_deploy_ok.txt ]; then
  echo "[APP] Already deployed, skipping."
  exit 0
fi

# -------------------------------------------------------------------
# VARIABLES INYECTADAS POR TERRAFORM (NO SENSIBLES)
# -------------------------------------------------------------------
DB_PRIVATE_IP="${db_private_ip}"         # IP privada instancia DATA
KAFKA_PRIVATE_IP="${kafka_private_ip}"   # IP privada instancia Kafka
ALB_DNS_NAME="${alb_dns_name}"           # DNS del ALB
# -------------------------------------------------------------------

if [ -z "$${DB_PRIVATE_IP}" ]; then
  echo "[ERROR] DB_PRIVATE_IP empty"
  exit 1
elif [ -z "$${ALB_DNS_NAME}" ]; then
  echo "[ERROR] ALB_DNS_NAME empty"
  exit 1
elif [ -z "$${KAFKA_PRIVATE_IP}" ]; then
  echo "[WARN] KAFKA_PRIVATE_IP empty"
fi

echo "[APP] Updating packages..."
yum update -y

echo "[APP] Installing Docker..."
amazon-linux-extras install docker -y

echo "[APP] Enabling Docker..."
systemctl enable docker
systemctl start docker
usermod -aG docker ec2-user

echo "[APP] Installing docker-compose..."
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" \
  -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

systemctl is-active --quiet docker || exit 1

# -------------------------------------------------------------------
# docker-compose (APP)
# -------------------------------------------------------------------
cat > docker-compose.app.yml <<YAML
version: "3.9"

services:
  web:
    image: juantulcanaza/nutrygym-web:qa-1
    container_name: nutrigym-web
    restart: unless-stopped
    networks:
      - nutrigym-network
  gateway:
    image: juantulcanaza/nutrygym-gateway:qa-3
    container_name: nutrigym-gateway
    ports:
      - "80:80"
    depends_on:
      - web
      - auth-service
      - user-profile-service
      - authorization-service
      - nutrition-form
      - plan-management
      - ai-generator-service
    restart: unless-stopped
    networks:
      - nutrigym-network

  auth-service:
    image: juantulcanaza/auth-service:qa-1
    env_file: ./.env.auth
    networks: [nutrigym-network]

  user-profile-service:
    image: juantulcanaza/user-profile-service:qa-1
    env_file: ./.env.user-profile
    networks: [nutrigym-network]

  authorization-service:
    image: juantulcanaza/authorization-service:qa-1
    env_file: ./.env.authz
    networks: [nutrigym-network]

  nutrition-form:
    image: juantulcanaza/nutrition-form-service:qa-1
    env_file: ./.env.nutrition
    networks: [nutrigym-network]

  plan-management:
    image: juantulcanaza/plan-management-service:qa-1
    env_file: ./.env.plans
    networks: [nutrigym-network]

  ai-generator-service:
    image: juantulcanaza/ai-generator-service:qa-1
    env_file: ./.env.ai
    networks: [nutrigym-network]

networks:
  nutrigym-network:
    driver: bridge
YAML

# -------------------------------------------------------------------
# ENV FILES (SANITIZADOS)
# -------------------------------------------------------------------

cat > .env.auth <<ENV
DB_HOST=$${DB_PRIVATE_IP}
DB_PORT=PUERTO_DB_AUTH_AQUI
DB_NAME=NOMBRE_DB_AQUI
DB_USER=USUARIO_DB_AQUI
DB_PASSWORD=PASSWORD_DB_AQUI
JWT_SECRET=AQUI_VA_TU_JWT_SECRET
JWT_ALGORITHM=HS256
PORT=PUERTO_AUTH_SERVICE
ALLOWED_ORIGINS=http://$${ALB_DNS_NAME}
ENV

cat > .env.user-profile <<ENV
DB_HOST=$${DB_PRIVATE_IP}
DB_PORT=PUERTO_DB_PROFILE_AQUI
DB_NAME=NOMBRE_DB_PROFILE
DB_USER=USUARIO_DB_PROFILE
DB_PASSWORD=PASSWORD_DB_PROFILE
JWT_SECRET=AQUI_VA_TU_JWT_SECRET
PORT=PUERTO_PROFILE_SERVICE
ALLOWED_ORIGINS=http://$${ALB_DNS_NAME}
ENV

cat > .env.authz <<ENV
JWT_SECRET=AQUI_VA_TU_JWT_SECRET
PORT=PUERTO_AUTHZ_SERVICE
ALLOWED_ORIGINS=http://$${ALB_DNS_NAME}
ENV

cat > .env.nutrition <<ENV
PORT=PUERTO_NUTRITION_SERVICE
DATABASE_URL=postgresql://USUARIO:PASSWORD@$${DB_PRIVATE_IP}:PUERTO_DB_NUTRITION/DB_NAME
REDIS_HOST=$${DB_PRIVATE_IP}
REDIS_PORT=PUERTO_REDIS
KAFKA_BOOTSTRAP_SERVERS=$${KAFKA_PRIVATE_IP}:PUERTO_KAFKA
JWT_SECRET=AQUI_VA_TU_JWT_SECRET
ENV

cat > .env.plans <<ENV
PORT=PUERTO_PLANS_SERVICE
DATABASE_URL=postgresql://USUARIO:PASSWORD@$${DB_PRIVATE_IP}:PUERTO_DB_PLANS/DB_NAME
REDIS_HOST=$${DB_PRIVATE_IP}
REDIS_PORT=PUERTO_REDIS
KAFKA_BOOTSTRAP_SERVERS=$${KAFKA_PRIVATE_IP}:PUERTO_KAFKA
INTERNAL_API_KEY=AQUI_VA_TU_API_KEY
ALLOWED_ORIGINS=http://$${ALB_DNS_NAME}
ENV

cat > .env.ai <<ENV
PORT=PUERTO_AI_SERVICE
KAFKA_BOOTSTRAP_SERVERS=$${KAFKA_PRIVATE_IP}:PUERTO_KAFKA
GROQ_API_KEY=AQUI_VA_TU_API_KEY
MONGO_URI=mongodb://$${DB_PRIVATE_IP}:PUERTO_MONGO
JWT_SECRET_KEY=AQUI_VA_TU_JWT_SECRET
INTERNAL_API_KEY=AQUI_VA_TU_API_KEY
ENV

cat > .env <<ENV
VITE_AUTH_API_URL=/api/auth
VITE_PROFILE_API_URL=/api/profile
VITE_AUTHZ_API_URL=/api/authz
VITE_NUTRITION_FORM_API_URL=/api/nutrition/api/v1
VITE_PLAN_MANAGEMENT_URL=/api/plans
ENV

/usr/local/bin/docker-compose -f docker-compose.app.yml pull
/usr/local/bin/docker-compose -f docker-compose.app.yml up -d

echo "NutryGym APP deployed OK" > /opt/nutrygym/app_deploy_ok.txt
