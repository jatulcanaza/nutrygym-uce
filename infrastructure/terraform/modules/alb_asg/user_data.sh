#!/bin/bash
set -euo pipefail

exec > >(tee -a /var/log/nutrygym-bootstrap.log) 2>&1
echo "[BOOT] $(date) Starting NutryGym bootstrap..."

APP_DIR="/opt/nutrygym"

echo "[BOOT] Updating packages..."
yum update -y

echo "[BOOT] Installing Docker..."
amazon-linux-extras install docker -y

echo "[BOOT] Enabling Docker..."
systemctl enable docker
systemctl start docker
usermod -aG docker ec2-user

echo "[BOOT] Installing docker-compose..."
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" \
  -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

echo "[BOOT] Creating app directory..."
mkdir -p "${APP_DIR}"
cd "${APP_DIR}"

systemctl is-active --quiet docker || (echo "[ERROR] Docker not active" && exit 1)

echo "[BOOT] Writing docker-compose.yml..."

cat > docker-compose.yml <<'YAML'
version: "3.9"

services:
  gateway:
    image: tu_usuario/nutrygym-gateway:TAG
    container_name: nutrigym-gateway
    ports:
      - "PUERTO_EXTERNO:PUERTO_INTERNO"
    depends_on:
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
    image: tu_usuario/auth-service:TAG
    container_name: auth-service
    env_file: ./.env.auth
    depends_on:
      - auth-db
    restart: unless-stopped
    networks:
      - nutrigym-network

  auth-db:
    image: postgres:VERSION
    container_name: auth-db
    environment:
      POSTGRES_DB: NOMBRE_DB
      POSTGRES_USER: USUARIO_DB
      POSTGRES_PASSWORD: PASSWORD_DB
    volumes:
      - auth_postgres_data:/var/lib/postgresql/data
    restart: unless-stopped
    networks:
      - nutrigym-network

  user-profile-service:
    image: tu_usuario/user-profile-service:TAG
    container_name: user-profile-service
    env_file: ./.env.user-profile
    restart: unless-stopped
    networks:
      - nutrigym-network

  user-profile-db:
    image: postgres:VERSION
    container_name: user-profile-db
    environment:
      POSTGRES_DB: NOMBRE_DB
      POSTGRES_USER: USUARIO_DB
      POSTGRES_PASSWORD: PASSWORD_DB
    restart: unless-stopped
    networks:
      - nutrigym-network

  authorization-service:
    image: tu_usuario/authorization-service:TAG
    container_name: authorization-service
    env_file: ./.env.authz
    restart: unless-stopped
    networks:
      - nutrigym-network

  nutrition-form:
    image: tu_usuario/nutrition-form-service:TAG
    container_name: nutrition-form
    env_file: ./.env.nutrition
    restart: unless-stopped
    networks:
      - nutrigym-network

  nutrition-postgres:
    image: postgres:VERSION
    container_name: nutrition-postgres
    environment:
      POSTGRES_DB: NOMBRE_DB
      POSTGRES_USER: USUARIO_DB
      POSTGRES_PASSWORD: PASSWORD_DB
    restart: unless-stopped
    networks:
      - nutrigym-network

  nutrition-redis:
    image: redis:VERSION
    container_name: nutrition-redis
    restart: unless-stopped
    networks:
      - nutrigym-network

  zookeeper:
    image: confluentinc/cp-zookeeper:VERSION
    container_name: nutrigym-zookeeper
    restart: unless-stopped
    networks:
      - nutrigym-network

  kafka:
    image: confluentinc/cp-kafka:VERSION
    container_name: nutrigym-kafka
    depends_on:
      - zookeeper
    restart: unless-stopped
    networks:
      - nutrigym-network

  plan-management:
    image: tu_usuario/plan-management-service:TAG
    container_name: plan-management
    env_file: ./.env.plans
    restart: unless-stopped
    networks:
      - nutrigym-network

  plan-postgres:
    image: postgres:VERSION
    container_name: plan-postgres
    environment:
      POSTGRES_DB: NOMBRE_DB
      POSTGRES_USER: USUARIO_DB
      POSTGRES_PASSWORD: PASSWORD_DB
    restart: unless-stopped
    networks:
      - nutrigym-network

  plan-redis:
    image: redis:VERSION
    container_name: plan-redis
    restart: unless-stopped
    networks:
      - nutrigym-network

  ai-generator-mongo:
    image: mongo:VERSION
    container_name: ai-generator-mongo
    restart: unless-stopped
    networks:
      - nutrigym-network

  ai-generator-service:
    image: tu_usuario/ai-generator-service:TAG
    container_name: ai-generator-service
    env_file: ./.env.ai
    restart: unless-stopped
    networks:
      - nutrigym-network

networks:
  nutrigym-network:
    driver: bridge

volumes:
  auth_postgres_data:
  user_profile_postgres_data:
  nutrition_postgres_data:
  plan_postgres_data:
  ai_mongo_data:
YAML

echo "[BOOT] Writing env template files..."

cat > .env.auth <<'ENV'
DB_HOST=HOST_DB
DB_PORT=PUERTO_DB
DB_NAME=NOMBRE_DB
DB_USER=USUARIO_DB
DB_PASSWORD=PASSWORD_DB
JWT_SECRET=TU_SECRET_AQUI
PORT=PUERTO_SERVICIO
ENV

cat > .env.user-profile <<'ENV'
DB_HOST=HOST_DB
DB_PORT=PUERTO_DB
DB_NAME=NOMBRE_DB
DB_USER=USUARIO_DB
DB_PASSWORD=PASSWORD_DB
JWT_SECRET=TU_SECRET_AQUI
PORT=PUERTO_SERVICIO
ENV

cat > .env.authz <<'ENV'
JWT_SECRET=TU_SECRET_AQUI
PORT=PUERTO_SERVICIO
ENV

cat > .env.nutrition <<'ENV'
PORT=PUERTO_SERVICIO
DATABASE_URL=postgresql://USUARIO:PASSWORD@HOST:PUERTO/DB
REDIS_HOST=HOST_REDIS
REDIS_PORT=PUERTO_REDIS
KAFKA_BOOTSTRAP_SERVERS=HOST_KAFKA:PUERTO
ENV

cat > .env.plans <<'ENV'
PORT=PUERTO_SERVICIO
DATABASE_URL=postgresql://USUARIO:PASSWORD@HOST:PUERTO/DB
ENV

cat > .env.ai <<'ENV'
PORT=PUERTO_SERVICIO
MONGO_URI=mongodb://HOST:PUERTO
ENV

echo "[BOOT] Pulling images..."
docker-compose pull

echo "[BOOT] Starting stack..."
docker-compose up -d

echo "[BOOT] Stack status..."
docker-compose ps || true

echo "NutryGym deployed OK" > /opt/nutrygym/deploy_ok.txt
echo "[BOOT] $(date) Done."
