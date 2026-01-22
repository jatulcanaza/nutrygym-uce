#!/bin/bash
set -eo pipefail

exec > >(tee -a /var/log/nutrygym-data-bootstrap.log) 2>&1
echo "[DATA] $(date) Starting NutryGym DATA bootstrap..."

DATA_DIR="/opt/nutrygym-data"
MOUNT_POINT="/data"

mkdir -p "$${DATA_DIR}"
cd "$${DATA_DIR}"

echo "[DATA] Updating packages..."
yum update -y
# ---- Site24x7 ----
echo "[MONITORING] Installing Site24x7 agent..."
cd /tmp
wget -q https://staticdownloads.site24x7.com/server/Site24x7FullStackAgent_LinuxIns.sh
chmod +x Site24x7FullStackAgent_LinuxIns.sh
bash Site24x7FullStackAgent_LinuxIns.sh \
  -i \
  -key= \
  -automation=true \
  -apm_insight=false
echo "[MONITORING] Site24x7 installed"
# ------------------

echo "[DATA] Installing Docker..."
amazon-linux-extras install docker -y

echo "[DATA] Enabling Docker..."
systemctl enable docker
systemctl start docker
usermod -aG docker ec2-user

echo "[DATA] Installing docker-compose..."
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" \
  -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

systemctl is-active --quiet docker || (echo "[ERROR] Docker not active" && exit 1)

# -------------------------------------------------------------------
# PERSISTENCIA REAL EN EBS
# -------------------------------------------------------------------
echo "[DATA] Detecting attached data disk..."
DEVICE=""

if lsblk | grep -q "nvme1n1"; then
  DEVICE="/dev/nvme1n1"
elif [ -b /dev/xvdf ]; then
  DEVICE="/dev/xvdf"
elif [ -b /dev/sdf ]; then
  DEVICE="/dev/sdf"
else
  echo "[DATA][WARN] Could not detect secondary disk automatically."
fi

mkdir -p "$${MOUNT_POINT}"

if [ -n "$${DEVICE}" ]; then
  if ! blkid "$${DEVICE}" >/dev/null 2>&1; then
    mkfs.xfs -f "$${DEVICE}"
  fi

  if ! mount | grep -q " $${MOUNT_POINT} "; then
    mount "$${DEVICE}" "$${MOUNT_POINT}"
  fi

  UUID=$(blkid -s UUID -o value "$${DEVICE}")
  grep -q "$${UUID}" /etc/fstab || \
    echo "UUID=$${UUID}  $${MOUNT_POINT}  xfs  defaults,nofail  0  2" >> /etc/fstab
else
  echo "[DATA][WARN] No device detected; persistence may NOT survive instance replacement."
fi

# -------------------------------------------------------------------
# ESTRUCTURA DE CARPETAS PERSISTENTES
# -------------------------------------------------------------------
mkdir -p $${MOUNT_POINT}/postgres/auth
mkdir -p $${MOUNT_POINT}/postgres/user_profile
mkdir -p $${MOUNT_POINT}/postgres/nutrition
mkdir -p $${MOUNT_POINT}/postgres/plans
mkdir -p $${MOUNT_POINT}/redis/nutrition
mkdir -p $${MOUNT_POINT}/redis/plans
mkdir -p $${MOUNT_POINT}/mongo

# -------------------------------------------------------------------
# docker-compose (DATA) - SOLO BDs (DATOS DE EJEMPLO)
# -------------------------------------------------------------------
echo "[DATA] Writing docker-compose.data.yml..."

cat > docker-compose.data.yml <<YAML
version: "3.9"

services:
  auth-db:
    image: postgres:15
    container_name: auth-db
    environment:
      POSTGRES_DB: EXAMPLE_AUTH_DB
      POSTGRES_USER: EXAMPLE_AUTH_USER
      POSTGRES_PASSWORD: EXAMPLE_AUTH_PASSWORD
    ports:
      - "YOUR_AUTH_DB_PORT:5432"
    volumes:
      - $${MOUNT_POINT}/postgres/auth:/var/lib/postgresql/data
    restart: unless-stopped

  user-profile-db:
    image: postgres:15
    container_name: user-profile-db
    environment:
      POSTGRES_DB: EXAMPLE_USER_PROFILE_DB
      POSTGRES_USER: EXAMPLE_USER_PROFILE_USER
      POSTGRES_PASSWORD: EXAMPLE_USER_PROFILE_PASSWORD
    ports:
      - "YOUR_USER_PROFILE_DB_PORT:5432"
    volumes:
      - $${MOUNT_POINT}/postgres/user_profile:/var/lib/postgresql/data
    restart: unless-stopped

  nutrition-postgres:
    image: postgres:15-alpine
    container_name: nutrition-postgres
    environment:
      POSTGRES_DB: EXAMPLE_NUTRITION_DB
      POSTGRES_USER: EXAMPLE_NUTRITION_USER
      POSTGRES_PASSWORD: EXAMPLE_NUTRITION_PASSWORD
    ports:
      - "YOUR_NUTRITION_DB_PORT:5432"
    volumes:
      - $${MOUNT_POINT}/postgres/nutrition:/var/lib/postgresql/data
    restart: unless-stopped

  plan-postgres:
    image: postgres:15-alpine
    container_name: plan-postgres
    environment:
      POSTGRES_DB: EXAMPLE_PLANS_DB
      POSTGRES_USER: EXAMPLE_PLANS_USER
      POSTGRES_PASSWORD: EXAMPLE_PLANS_PASSWORD
    ports:
      - "YOUR_PLANS_DB_PORT:5432"
    volumes:
      - $${MOUNT_POINT}/postgres/plans:/var/lib/postgresql/data
    restart: unless-stopped

  nutrition-redis:
    image: redis:7-alpine
    container_name: nutrition-redis
    command: ["redis-server", "--appendonly", "yes"]
    ports:
      - "YOUR_NUTRITION_REDIS_PORT:6379"
    volumes:
      - $${MOUNT_POINT}/redis/nutrition:/data
    restart: unless-stopped

  plan-redis:
    image: redis:7-alpine
    container_name: plan-redis
    command: ["redis-server", "--appendonly", "yes"]
    ports:
      - "YOUR_PLANS_REDIS_PORT:6379"
    volumes:
      - $${MOUNT_POINT}/redis/plans:/data
    restart: unless-stopped

  ai-generator-mongo:
    image: mongo:7.0
    container_name: ai-generator-mongo
    ports:
      - "YOUR_MONGO_PORT:27017"
    volumes:
      - $${MOUNT_POINT}/mongo:/data/db
    restart: unless-stopped
YAML

echo "[DATA] Pulling images..."
/usr/local/bin/docker-compose -f docker-compose.data.yml pull

echo "[DATA] Starting DATA stack..."
/usr/local/bin/docker-compose -f docker-compose.data.yml up -d

echo "[DATA] Stack status..."
/usr/local/bin/docker-compose -f docker-compose.data.yml ps || true

echo "NutryGym DATA deployed OK" > /opt/nutrygym-data/data_deploy_ok.txt
echo "[DATA] $(date) Done."
