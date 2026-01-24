#!/bin/bash
set -euo pipefail
LOG=/var/log/nutrygym-kafka-bootstrap.log
mkdir -p /var/log
touch "$LOG"
chmod 644 "$LOG"
exec >>"$LOG" 2>&1
echo "[KAFKA] $(date) Starting Kafka bootstrap..."

APP_DIR="/opt/nutrygym-kafka"
mkdir -p "$${APP_DIR}"
cd "$${APP_DIR}"

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

amazon-linux-extras install docker -y
systemctl enable docker
systemctl start docker
usermod -aG docker ec2-user

curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" \
  -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# IP privada real de esta instancia (para advertised listeners)
KAFKA_PRIVATE_IP=$(curl -s http://169.254.169.254/latest/meta-data/local-ipv4)
echo "[KAFKA] Private IP: $${KAFKA_PRIVATE_IP}"

cat > docker-compose.kafka.yml <<YAML
version: "3.9"
services:
  zookeeper:
    image: confluentinc/cp-zookeeper:7.5.3
    container_name: nutrigym-zookeeper
    environment:
      ZOOKEEPER_CLIENT_PORT: YOUR_PORT
      ZOOKEEPER_TICK_TIME: YOUR_KEY_HERE
      ZOOKEEPER_SERVER_ID: YOUR_KEY_HERE
    restart: unless-stopped

  kafka:
    image: confluentinc/cp-kafka:7.5.3
    container_name: nutrigym-kafka
    depends_on:
      - zookeeper
    ports:
      - "YOUR_PORT:YOUR_PORT"
    environment:
      KAFKA_BROKER_ID: YOUR_KEY_HERE
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:YOUR_PORT
      # Listener interno (contenedores) + externo (VPC)
      KAFKA_LISTENERS: INTERNAL://0.0.0.0:YOUR_PORT,EXTERNAL://0.0.0.0:YOUR_PORT
      KAFKA_ADVERTISED_LISTENERS: INTERNAL://kafka:YOUR_PORT,EXTERNAL://$${KAFKA_PRIVATE_IP}:YOUR_PORT
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: INTERNAL:PLAINTEXT,EXTERNAL:PLAINTEXT
      KAFKA_INTER_BROKER_LISTENER_NAME: INTERNAL
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: YOUR_KEY_HERE
      KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: YOUR_KEY_HERE
      KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: YOUR_KEY_HERE
      KAFKA_AUTO_CREATE_TOPICS_ENABLE: "true"
    restart: unless-stopped
YAML

/usr/local/bin/docker-compose -f docker-compose.kafka.yml pull
/usr/local/bin/docker-compose -f docker-compose.kafka.yml up -d
/usr/local/bin/docker-compose -f docker-compose.kafka.yml ps || true

echo "NutryGym Kafka deployed OK" > /opt/nutrygym-kafka/kafka_deploy_ok.txt
echo "[KAFKA] $(date) Done."
