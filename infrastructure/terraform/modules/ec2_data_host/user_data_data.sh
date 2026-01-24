#!/bin/bash
set -euo pipefail
LOG=/var/log/nutrygym-data-bootstrap.log
mkdir -p /var/log
touch "$LOG"
chmod 644 "$LOG"
exec >>"$LOG" 2>&1
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
  -key=YOUR_KEY_HERE \
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
# Asumimos que Terraform adjunta un volumen (por ejemplo /dev/xvdf o /dev/nvme1n1)
# NOTA: el nombre exacto del device puede variar en Nitro (nvme).
# -------------------------------------------------------------------
echo "[DATA] Detecting attached data disk..."
DEVICE=""
# Prioridad: NVMe común en instancias Nitro
if lsblk | grep -q "nvme1n1"; then
  DEVICE="/dev/nvme1n1"
elif [ -b /dev/xvdf ]; then
  DEVICE="/dev/xvdf"
elif [ -b /dev/sdf ]; then
  DEVICE="/dev/sdf"
else
  echo "[DATA][WARN] Could not detect secondary disk automatically."
  echo "[DATA][WARN] You may need to set DEVICE manually."
fi

mkdir -p "$${MOUNT_POINT}"

if [ -n "$${DEVICE}" ]; then
  echo "[DATA] Using device: $${DEVICE}"
  # Si no tiene filesystem, lo formatea (XFS recomendado en Amazon Linux)
  if ! blkid "$${DEVICE}" >/dev/null 2>&1; then
    echo "[DATA] Formatting $${DEVICE} with XFS..."
    mkfs.xfs -f "$${DEVICE}"
  fi
  # Monta si no está montado
  if ! mount | grep -q " $${MOUNT_POINT} "; then
    echo "[DATA] Mounting $${DEVICE} to $${MOUNT_POINT}..."
    mount "$${DEVICE}" "$${MOUNT_POINT}"
  fi
  # Persistir en fstab
  UUID=$(blkid -s UUID -o value "$${DEVICE}")
  if ! grep -q "$${UUID}" /etc/fstab; then
    echo "[DATA] Writing fstab entry..."
    echo "UUID=$${UUID}  $${MOUNT_POINT}  xfs  defaults,nofail  0  2" >> /etc/fstab
  fi
else
  echo "[DATA][WARN] No device detected; persistence may NOT survive instance replacement."
fi

# Estructura de carpetas persistentes
mkdir -p $${MOUNT_POINT}/postgres/auth
mkdir -p $${MOUNT_POINT}/postgres/user_profile
mkdir -p $${MOUNT_POINT}/postgres/nutrition
mkdir -p $${MOUNT_POINT}/postgres/plans
mkdir -p $${MOUNT_POINT}/redis/nutrition
mkdir -p $${MOUNT_POINT}/redis/plans
mkdir -p $${MOUNT_POINT}/mongo

# -------------------------------------------------------------------
# docker-compose (DATA) - SOLO BDs
# OJO: muchos Postgres => puertos host distintos:
#   (reemplazados por placeholders para evitar exponer puertos específicos)
# Redis también:
#   (reemplazados por placeholders para evitar exponer puertos específicos)
# -------------------------------------------------------------------
echo "[DATA] Writing docker-compose.data.yml..."
cat > docker-compose.data.yml <<YAML
version: "3.9"
services:
  auth-db:
    image: postgres:15
    container_name: auth-db
    environment:
      POSTGRES_DB: auth_db
      POSTGRES_USER: YOUR_KEY_HERE
      POSTGRES_PASSWORD: YOUR_KEY_HERE
    ports:
      - "YOUR_PORT:YOUR_PORT"
    volumes:
      - $${MOUNT_POINT}/postgres/auth:/var/lib/postgresql/data
    restart: unless-stopped

  user-profile-db:
    image: postgres:15
    container_name: user-profile-db
    environment:
      POSTGRES_DB: user_profile_db
      POSTGRES_USER: YOUR_KEY_HERE
      POSTGRES_PASSWORD: YOUR_KEY_HERE
    ports:
      - "YOUR_PORT:YOUR_PORT"
    volumes:
      - $${MOUNT_POINT}/postgres/user_profile:/var/lib/postgresql/data
    restart: unless-stopped

  nutrition-postgres:
    image: postgres:15-alpine
    container_name: nutrition-postgres
    environment:
      POSTGRES_DB: nutrigym_nutrition
      POSTGRES_USER: YOUR_KEY_HERE
      POSTGRES_PASSWORD: YOUR_KEY_HERE
    ports:
      - "YOUR_PORT:YOUR_PORT"
    volumes:
      - $${MOUNT_POINT}/postgres/nutrition:/var/lib/postgresql/data
    restart: unless-stopped

  plan-postgres:
    image: postgres:15-alpine
    container_name: plan-postgres
    environment:
      POSTGRES_DB: nutrigym_plans
      POSTGRES_USER: YOUR_KEY_HERE
      POSTGRES_PASSWORD: YOUR_KEY_HERE
    ports:
      - "YOUR_PORT:YOUR_PORT"
    volumes:
      - $${MOUNT_POINT}/postgres/plans:/var/lib/postgresql/data
    restart: unless-stopped

  nutrition-redis:
    image: redis:7-alpine
    container_name: nutrition-redis
    command: ["redis-server", "--appendonly", "yes"]
    ports:
      - "YOUR_PORT:YOUR_PORT"
    volumes:
      - $${MOUNT_POINT}/redis/nutrition:/data
    restart: unless-stopped

  plan-redis:
    image: redis:7-alpine
    container_name: plan-redis
    command: ["redis-server", "--appendonly", "yes"]
    ports:
      - "YOUR_PORT:YOUR_PORT"
    volumes:
      - $${MOUNT_POINT}/redis/plans:/data
    restart: unless-stopped

  ai-generator-mongo:
    image: mongo:7.0
    container_name: ai-generator-mongo
    ports:
      - "YOUR_PORT:YOUR_PORT"
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
