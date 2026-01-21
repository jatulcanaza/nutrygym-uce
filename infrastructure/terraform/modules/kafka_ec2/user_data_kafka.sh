#!/bin/bash
set -eo pipefail

exec > >(tee -a /var/log/nutrygym-kafka-bootstrap.log) 2>&1
echo "[KAFKA] $(date) Starting Kafka bootstrap..."

APP_DIR="/opt/nutrygym-kafka"
mkdir -p "$${APP_DIR}"
cd "$${APP_DIR}"

yum update -y
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
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
      ZOOKEEPER_SERVER_ID: 1
    restart: unless-stopped

  kafka:
    image: confluentinc/cp-kafka:7.5.3
    container_name: nutrigym-kafka
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181

      # Listener interno (contenedores) + externo (VPC)
      KAFKA_LISTENERS: INTERNAL://0.0.0.0:9093,EXTERNAL://0.0.0.0:9092
      KAFKA_ADVERTISED_LISTENERS: INTERNAL://kafka:9093,EXTERNAL://$${KAFKA_PRIVATE_IP}:9092
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: INTERNAL:PLAINTEXT,EXTERNAL:PLAINTEXT
      KAFKA_INTER_BROKER_LISTENER_NAME: INTERNAL

      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: 1
      KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 1
      KAFKA_AUTO_CREATE_TOPICS_ENABLE: "true"
    restart: unless-stopped
YAML

/usr/local/bin/docker-compose -f docker-compose.kafka.yml pull
/usr/local/bin/docker-compose -f docker-compose.kafka.yml up -d
/usr/local/bin/docker-compose -f docker-compose.kafka.yml ps || true

echo "NutryGym Kafka deployed OK" > /opt/nutrygym-kafka/kafka_deploy_ok.txt
echo "[KAFKA] $(date) Done."
