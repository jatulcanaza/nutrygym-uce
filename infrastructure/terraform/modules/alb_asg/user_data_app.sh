#!/bin/bash
set -euo pipefail
LOG=/var/log/nutrygym-app-bootstrap.log
mkdir -p /var/log
touch "$LOG"
chmod 644 "$LOG"
exec >>"$LOG" 2>&1
echo "[APP] $(date) Starting NutryGym APP bootstrap..."

APP_DIR="/opt/nutrygym"
mkdir -p "$${APP_DIR}"
cd "$${APP_DIR}"
if [ -f /opt/nutrygym/app_deploy_ok.txt ]; then
  echo "[APP] Already deployed, skipping."
  exit 0
fi

# -------------------------------------------------------------------
# IMPORTANTES (inyectados por Terraform templatefile)
# NO edites aquí a mano si lo vas a pasar por templatefile()
# -------------------------------------------------------------------
DB_PRIVATE_IP="${db_private_ip}"         # <-- IP privada de la instancia DATA (output db_private_ip)
KAFKA_PRIVATE_IP="${kafka_private_ip}"   # <-- IP privada de la instancia Kafka (output kafka_private_ip)
ALB_DNS_NAME="${alb_dns_name}"           # <-- DNS del ALB (output alb_dns_name)
# -------------------------------------------------------------------

# Reemplazar las 3 líneas de verificación con:
if [ -z "$${DB_PRIVATE_IP}" ]; then
  echo "[ERROR] DB_PRIVATE_IP empty"
  exit 1
elif [ -z "$${ALB_DNS_NAME}" ]; then
  echo "[ERROR] ALB_DNS_NAME empty"
  exit 1
elif [ -z "$${KAFKA_PRIVATE_IP}" ]; then
  echo "[APP][WARN] KAFKA_PRIVATE_IP empty. Kafka features may fail."
fi

echo "[APP] Updating packages..."
yum update -y

# ---- Site24x7 ----
echo "[MONITORING] Installing Site24x7 agent..."
cd /tmp
wget -q https://staticdownloads.site24x7.com/server/Site24x7FullStackAgent_LinuxIns.sh
chmod +x Site24x7FullStackAgent_LinuxIns.sh
bash Site24x7FullStackAgent_LinuxIns.sh \
  -i \
  -key=YOUR_KEY_HERE \
  -automation=true \
  -apm_insight=false
echo "[MONITORING] Site24x7 installed"
# ------------------

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

systemctl is-active --quiet docker || (echo "[ERROR] Docker not active" && exit 1)

# -------------------------------------------------------------------
# docker-compose (APP) - SIN BD
# Kafka está EN OTRA INSTANCIA (kafka_ec2), por eso NO lo levantamos aquí.
# -------------------------------------------------------------------
echo "[APP] Writing docker-compose.app.yml..."
cat > docker-compose.app.yml <<YAML
version: "3.9"
services:
  web:
    image: juantulcanaza/nutrygym-web:qa
    container_name: nutrigym-web
    restart: unless-stopped
    networks:
      - nutrigym-network

  gateway:
    image: juantulcanaza/nutrygym-gateway:qa
    container_name: nutrigym-gateway
    ports:
      - "YOUR_PORT:YOUR_PORT"
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
    image: juantulcanaza/auth-service:qa
    container_name: auth-service
    env_file: ./.env.auth
    restart: unless-stopped
    networks:
      - nutrigym-network

  user-profile-service:
    image: juantulcanaza/user-profile-service:qa
    container_name: user-profile-service
    env_file: ./.env.user-profile
    restart: unless-stopped
    networks:
      - nutrigym-network

  authorization-service:
    image: juantulcanaza/authorization-service:qa
    container_name: authorization-service
    env_file: ./.env.authz
    restart: unless-stopped
    networks:
      - nutrigym-network

  nutrition-form:
    image: juantulcanaza/nutrition-form-service:qa
    container_name: nutrition-form
    env_file: ./.env.nutrition
    restart: unless-stopped
    networks:
      - nutrigym-network

  plan-management:
    image: juantulcanaza/plan-management-service:qa
    container_name: plan-management
    env_file: ./.env.plans
    restart: unless-stopped
    networks:
      - nutrigym-network

  ai-generator-service:
    image: juantulcanaza/ai-generator-service:qa
    container_name: ai-generator-service
    env_file: ./.env.ai
    restart: unless-stopped
    networks:
      - nutrigym-network

  rabbitmq:
    image: rabbitmq:3-management
    container_name: nutrigym-rabbitmq
    environment:
      RABBITMQ_DEFAULT_USER: YOUR_KEY_HERE
      RABBITMQ_DEFAULT_PASS: YOUR_KEY_HERE
    ports:
      - "YOUR_PORT:YOUR_PORT"
      - "YOUR_PORT:YOUR_PORT"
    healthcheck:
      test: ["CMD-SHELL", "rabbitmq-diagnostics -q ping"]
      interval: 10s
      timeout: 10s
      retries: 30
    restart: unless-stopped
    networks:
      - nutrigym-network

  mosquitto:
    image: eclipse-mosquitto:2
    container_name: notification-mosquitto
    ports:
      - "YOUR_PORT:YOUR_PORT"
    volumes:
      - ./mosquitto.conf:/mosquitto/config/mosquitto.conf:ro
    restart: unless-stopped
    networks:
      - nutrigym-network

  notification-service:
    image: juantulcanaza/notification-service:qa
    container_name: notification-service
    env_file: ./.env.notifications
    ports:
      - "YOUR_PORT:YOUR_PORT"
    depends_on:
      rabbitmq:
        condition: service_healthy
      mosquitto:
        condition: service_started
    restart: unless-stopped
    networks:
      - nutrigym-network

  notification-dashboard:
    image: juantulcanaza/notification-dashboard:qa
    container_name: notification-dashboard
    env_file: ./.env.dashboard
    ports:
      - "YOUR_PORT:YOUR_PORT"
    depends_on:
      - notification-service
      - mosquitto
    restart: unless-stopped
    networks:
      - nutrigym-network

networks:
  nutrigym-network:
    driver: bridge
YAML

cat > mosquitto.conf <<'CONF'
persistence true
persistence_location /mosquitto/data/
log_dest stdout
listener YOUR_PORT
allow_anonymous true
CONF

# -------------------------------------------------------------------
# ENV files (APP) apuntando a DATA por IP/puerto (host ports)
# -------------------------------------------------------------------
echo "[APP] Writing env files..."

cat > .env.auth <<ENV
DB_HOST=$${DB_PRIVATE_IP}
DB_PORT=YOUR_PORT
DB_NAME=auth_db
DB_USER=YOUR_KEY_HERE
DB_PASSWORD=YOUR_KEY_HERE
JWT_SECRET=YOUR_KEY_HERE
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=YOUR_KEY_HERE
REFRESH_TOKEN_EXPIRE_DAYS=YOUR_KEY_HERE
PORT=YOUR_PORT
NODE_ENV=qa
ALLOWED_EMAIL_DOMAIN=uce.edu.ec
ALLOWED_ORIGINS=http://$${ALB_DNS_NAME}
LOG_LEVEL=INFO
ENV

cat > .env.user-profile <<ENV
DB_HOST=$${DB_PRIVATE_IP}
DB_PORT=YOUR_PORT
DB_NAME=user_profile_db
DB_USER=YOUR_KEY_HERE
DB_PASSWORD=YOUR_KEY_HERE
JWT_SECRET=YOUR_KEY_HERE
JWT_ALGORITHM=HS256
PORT=YOUR_PORT
SERVICE_NAME=user-profile-service
ALLOWED_ORIGINS=http://$${ALB_DNS_NAME}
ENV

cat > .env.authz <<ENV
JWT_SECRET=YOUR_KEY_HERE
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=YOUR_KEY_HERE
REFRESH_TOKEN_EXPIRE_DAYS=YOUR_KEY_HERE
PORT=YOUR_PORT
SERVICE_NAME=role-permission-service
LOG_LEVEL=INFO
ALLOWED_ORIGINS=http://$${ALB_DNS_NAME}
ENV

cat > .env.nutrition <<ENV
PORT=YOUR_PORT
DATABASE_URL=postgresql://YOUR_KEY_HERE:YOUR_KEY_HERE@$${DB_PRIVATE_IP}:YOUR_PORT/nutrigym_nutrition
JWT_SECRET=YOUR_KEY_HERE
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=YOUR_KEY_HERE
REFRESH_TOKEN_EXPIRE_DAYS=YOUR_KEY_HERE
REDIS_HOST=$${DB_PRIVATE_IP}
REDIS_PORT=YOUR_PORT
KAFKA_BOOTSTRAP_SERVERS=$${KAFKA_PRIVATE_IP}:YOUR_PORT
KAFKA_TOPIC_NUTRITION_EVENTS=nutrition.events
KAFKA_CLIENT_ID=nutrition-form-service
LOG_LEVEL=INFO
ENVIRONMENT=qa
API_PREFIX=/api/v1
ENABLE_KAFKA=true
ENABLE_REDIS_CACHE=true
ENABLE_RATE_LIMITING=false
CORS_ORIGINS=["http://$${ALB_DNS_NAME}"]
ENV

cat > .env.plans <<ENV
PORT=YOUR_PORT
DATABASE_URL=postgresql://YOUR_KEY_HERE:YOUR_KEY_HERE@$${DB_PRIVATE_IP}:YOUR_PORT/nutrigym_plans
JWT_SECRET=YOUR_KEY_HERE
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=YOUR_KEY_HERE
REDIS_HOST=$${DB_PRIVATE_IP}
REDIS_PORT=YOUR_PORT
KAFKA_BOOTSTRAP_SERVERS=$${KAFKA_PRIVATE_IP}:YOUR_PORT
KAFKA_TOPIC_PLAN_EVENTS=plan.events
KAFKA_CLIENT_ID=plan-management-service
AUTH_SERVICE_URL=http://auth-service:YOUR_PORT
USER_PROFILE_SERVICE_URL=http://user-profile-service:YOUR_PORT
NUTRITION_FORM_SERVICE_URL=http://nutrition-form:YOUR_PORT
AI_GENERATOR_SERVICE_URL=http://ai-generator-service:YOUR_PORT
LOG_LEVEL=INFO
ENVIRONMENT=qa
ENABLE_REDIS_CACHE=true
INTERNAL_API_KEY=YOUR_KEY_HERE
ALLOWED_ORIGINS=http://$${ALB_DNS_NAME}
RABBITMQ_URL=amqp://YOUR_KEY_HERE:YOUR_KEY_HERE@rabbitmq:YOUR_PORT/
NOTIF_QUEUE=notifications.queue
ENV

cat > .env.ai <<ENV
PORT=YOUR_PORT
KAFKA_BOOTSTRAP_SERVERS=$${KAFKA_PRIVATE_IP}:YOUR_PORT
KAFKA_TOPIC_GENERATE=ai.generate
GROQ_API_KEY=YOUR_KEY_HERE
GROQ_MODEL=YOUR_KEY_HERE
MONGO_URI=mongodb://$${DB_PRIVATE_IP}:YOUR_PORT
MONGO_DB=nutrigym_ai
PLAN_MANAGEMENT_SERVICE_URL=http://plan-management:YOUR_PORT
SYSTEM_JWT_TOKEN=YOUR_KEY_HERE
JWT_SECRET_KEY=YOUR_KEY_HERE
JWT_ALGORITHM=HS256
INTERNAL_API_KEY=YOUR_KEY_HERE
ENV

cat > .env <<ENV
VITE_AUTH_API_URL=/api/auth
VITE_PROFILE_API_URL=/api/profile
VITE_AUTHZ_API_URL=/api/authz
VITE_NUTRITION_FORM_API_URL=/api/nutrition/api/v1
VITE_PLAN_MANAGEMENT_URL=/api/plans
ENV

cat > .env.notifications <<ENV
SERVICE_NAME=notification-service
LOG_LEVEL=INFO

# RabbitMQ (dentro de la misma red docker)
RABBITMQ_URL=amqp://YOUR_KEY_HERE:YOUR_KEY_HERE@rabbitmq:YOUR_PORT/
RABBITMQ_QUEUE=notifications.queue
RABBITMQ_PREFETCH=YOUR_KEY_HERE
CONSUMER_RETRY_SECONDS=YOUR_KEY_HERE

# MQTT
MQTT_HOST=mosquitto
MQTT_PORT=YOUR_PORT
MQTT_TOPIC=nutrygym/notifications
MQTT_QOS=YOUR_KEY_HERE

# SMTP (idealmente venir de SSM/Secrets, aquí solo placeholder)
SMTP_HOST=YOUR_KEY_HERE
SMTP_PORT=YOUR_PORT
SMTP_USER=YOUR_KEY_HERE
SMTP_PASS=YOUR_KEY_HERE
SMTP_FROM=YOUR_KEY_HERE
SMTP_USE_TLS=true
MAX_EMAIL_BODY_CHARS=YOUR_KEY_HERE

ADMIN_EMAIL=YOUR_KEY_HERE
SEND_USER_EMAILS=true
SEND_ADMIN_ALERTS=true
ADMIN_ALERT_SEVERITIES=info,warning,error
ENV

cat > .env.dashboard <<ENV
PORT=YOUR_PORT
MQTT_HOST=mosquitto
MQTT_PORT=YOUR_PORT
MQTT_TOPIC=nutrygym/notifications
LOG_LEVEL=INFO
ENV

echo "[APP] Pulling images..."
/usr/local/bin/docker-compose -f docker-compose.app.yml pull

echo "[APP] Starting APP stack..."
/usr/local/bin/docker-compose -f docker-compose.app.yml up -d

echo "[APP] Stack status..."
/usr/local/bin/docker-compose -f docker-compose.app.yml ps || true

echo "NutryGym APP deployed OK" > /opt/nutrygym/app_deploy_ok.txt
echo "[APP] $(date) Done."
