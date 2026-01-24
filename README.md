# 🥗 NutryGym UCE - Nutrition & Fitness Platform

<div align="center">

**A comprehensive nutrition and fitness platform with microservices architecture, AI, and AWS deployment**

[![Tech Stack](https://img.shields.io/badge/Built%20with-React%2B%2BNode%2B%2BPython%2B%2BDocker-blue)](#tech-stack)
[![Architecture](https://img.shields.io/badge/Architecture-Microservices-green)](#architecture)
[![Project Type](https://img.shields.io/badge/Type-Academic-orange)]()

**Academic Project - Central University of Ecuador (UCE)**

[Full Documentation](#documentation) • [Installation](#installation-and-setup) • [Architecture](#architecture) • [Services](#backend-services) • [Deployment](#deployment-on-aws)

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Backend Services](#backend-services)
- [Frontend Applications](#frontend-applications)
- [Installation and Setup](#installation-and-setup)
- [Local Execution](#local-execution)
- [Deployment on AWS](#deployment-on-aws)
- [Environment Variables](#environment-variables)
- [Documentation](#documentation)
- [Contributing](#contributing)

---

## 📱 Overview

**NutryGym** is a comprehensive platform designed for nutrition and fitness management within the Central University of Ecuador ecosystem. It includes:

✅ **Institutional authentication** with @uce.edu.ec email  
✅ **Personalized nutrition plans** generated with AI  
✅ **Role and permission management** by user  
✅ **Complete user profile** with biometric data  
✅ **Real-time notifications** (MQTT + Email)  
✅ **Administrative dashboard** for monitoring  
✅ **Responsive web application** (React + Vite)  
✅ **Mobile application** (React Native / Expo)  
✅ **Desktop app** for advanced analysis  

---

## 🛠️ Tech Stack

### **Frontend**
| Technology | Purpose |
|---|---|
| **React 19** | Web user interface |
| **TypeScript** | Type-safe development |
| **Vite** | Fast and modern build tool |
| **Tailwind CSS** | Responsive design |
| **React Router** | Web navigation |
| **Expo / React Native** | Native mobile apps |

### **Backend - Microservices**
| Service | Technology | Port |
|---|---|---|
| **Auth Service** | FastAPI + PostgreSQL + JWT | 3001 |
| **User Profile Service** | FastAPI + PostgreSQL | 3002 |
| **Plan Management Service** | FastAPI + PostgreSQL | 3003 |
| **Nutrition Form Service** | FastAPI + PostgreSQL | 3004 |
| **Role Permission Service** | FastAPI + PostgreSQL | 3005 |
| **AI Generator Service** | FastAPI + Python ML | 3006 |
| **Notification Service** | FastAPI + RabbitMQ + MQTT | 3011 |
| **Notification Dashboard** | FastAPI + WebSocket | 3012 |

### **Infrastructure**
| Component | Purpose |
|---|---|
| **Docker & Docker Compose** | Containerization |
| **PostgreSQL 15** | Relational database |
| **RabbitMQ** | Message broker (events) |
| **Mosquitto (MQTT)** | Real-time notifications |
| **SMTP (Gmail)** | Email delivery |
| **Nginx** | Reverse proxy / Gateway |
| **Terraform** | Infrastructure as Code (AWS) |
| **AWS (EC2, ALB, ASG)** | Production deployment |

### **Package Management & Monorepo**
| Tool | Use |
|---|---|
| **Turbo** | Monorepo build system |
| **npm workspaces** | Dependency management |
| **ESLint** | Linting |

---

## 🏗️ Architecture

### **Component Diagram**

```
┌─────────────────────────────────────────────────────────────┐
│                    END USER                                  │
└─────────────────────────────────────────────────────────────┘
           │                    │                    │
      Web App              Mobile App            Desktop App
   (React + Vite)      (React Native)         (Electron)
           │                    │                    │
           └────────────────────┼────────────────────┘
                                │
                          ┌──────────────┐
                          │  Gateway     │
                          │  (Nginx)     │
                          │ :8080        │
                          └──────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
   ┌─────────┐        ┌──────────────────┐    ┌──────────────┐
   │Auth Svc │        │ API Gateway      │    │ Other Svcs   │
   │:3001    │        │ + Middleware     │    │              │
   └─────────┘        └──────────────────┘    └──────────────┘
        │                      │
   Auth DB            User Svc │ Plan Svc │ AI Svc │ etc.
 (Postgres)          (Microservices)
                              │
        ┌─────────────────────┼─────────────────────┐
        │         │            │          │          │
   ┌────────┐ ┌─────────┐ ┌──────────┐ ┌──────┐ ┌────────┐
   │User DB │ │Plan DB  │ │Nutrition│ │Role  │ │Notif   │
   │        │ │         │ │Form DB  │ │ Perm │ │Service │
   └────────┘ └─────────┘ └──────────┘ │  DB  │ └────────┘
                                        └──────┘      │
                                                      │
                                        ┌─────────────┼──────────────┐
                                        │             │              │
                                    RabbitMQ      MQTT Broker     Email
                                    (Events)     (Mosquitto)    (SMTP)
```

### **Communication Patterns**

#### **Synchronous (REST/HTTP)**
- Client → Gateway → Microservice
- Immediate response
- Simple read/write requests

#### **Asynchronous (Event-Driven)**
- Microservice → RabbitMQ → Notification Service
- Service decoupling
- Used for: notifications, audit, batch processing

#### **Real-Time (WebSocket/MQTT)**
- Notification Service → MQTT → Clients
- Live dashboard
- Real-time updates

---

## 📂 Project Structure

```
nutrygym-uce/
│
├── 📱 apps/                          # Frontend applications
│   ├── web/                          # Web app (React + Vite)
│   │   ├── src/
│   │   │   ├── components/           # Reusable components
│   │   │   ├── pages/                # Routes/pages
│   │   │   ├── context/              # Context API
│   │   │   ├── api/                  # HTTP services
│   │   │   └── assets/               # Images, styles
│   │   ├── vite.config.ts
│   │   ├── tsconfig.json
│   │   └── package.json
│   │
│   ├── mobile/                       # Mobile app (Expo/React Native)
│   │   └── mobile/
│   │       ├── app/                  # Navigation stack
│   │       ├── components/
│   │       ├── screens/
│   │       ├── assets/
│   │       ├── app.json              # Expo config
│   │       └── package.json
│   │
│   └── desktop/                      # Desktop app (Electron)
│       ├── main.js                   # Main process
│       ├── preload.js                # Preload script
│       ├── offline.html              # Offline support
│       └── assets/
│
├── 🔌 services/                      # Backend microservices
│   ├── auth-service/                 # JWT Authentication
│   │   ├── app/
│   │   │   ├── core/                 # DB & security config
│   │   │   ├── models/               # SQLAlchemy models
│   │   │   ├── routes/               # Endpoints
│   │   │   └── services/             # Business logic
│   │   ├── main.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   │
│   ├── user-profile-service/         # User profile management
│   │   └── [similar structure]
│   │
│   ├── plan-management-service/      # Nutrition plans
│   │   └── [similar structure]
│   │
│   ├── nutrition-form-service/       # Nutrition forms
│   │   └── [similar structure]
│   │
│   ├── role_permission-service/      # RBAC
│   │   └── [similar structure]
│   │
│   ├── ai-generator-service/         # AI-generated plans
│   │   ├── app/
│   │   └── requirements.txt
│   │
│   ├── notification-service/         # Async notifications
│   │   ├── main.py
│   │   ├── requirements.txt
│   │   └── mosquitto.conf            # MQTT config
│   │
│   └── notification-dashboard/       # Real-time dashboard
│       └── [similar structure]
│
├── 🏗️ infrastructure/                # Infrastructure as Code
│   └── terraform/
│       ├── envs/
│       │   ├── qa/                   # QA environment
│       │   └── prod/                 # Production
│       └── modules/                  # Reusable modules
│           ├── alb_asg/              # Load Balancer + Auto Scaling
│           ├── bastion/              # Bastion host
│           ├── ec2_data_host/        # Data hosts
│           ├── gateway/              # API Gateway
│           ├── kafka_ec2/            # Event streaming
│           ├── observability/        # Monitoring
│           ├── security-groups/      # Security
│           └── ...
│
├── 🔧 ops/                           # Operations
│   ├── backup/                       # Backup scripts
│   ├── docker/                       # Docker configs for prod
│   └── load-test/                    # Load tests (k6)
│
├── 📚 docs/                          # Documentation
│   └── {diagrams}/                   # Diagrams
│
├── 📄 docker-compose.global.yml      # Local orchestration
├── 📄 docker-compose.global.qa.yml   # QA orchestration
├── 📄 turbo.json                     # Monorepo config
├── 📄 package.json                   # Root dependencies
└── 📄 README.md                      # This file
```

---

## 🔌 Backend Services

### **1. Auth Service** 🔐
**Responsible for:** Authentication & identity  
**Port:** 3001  
**Technology:** FastAPI + PostgreSQL + JWT  
**Features:**
- Registration with `@uce.edu.ec` emails only
- JWT tokens (access + refresh)
- bcrypt encryption
- Configurable CORS

**Main Endpoints:**
```
POST   /auth/register   - Register new user
POST   /auth/login      - Login & token generation
POST   /auth/refresh    - Refresh access token
POST   /auth/logout     - Logout
GET    /auth/me         - Get current user
GET    /users/          - List users
GET    /users/{id}      - Get user by ID
```

**Documentation:** [services/auth-service/README.md](services/auth-service/README.md)

---

### **2. User Profile Service** 👤
**Responsible for:** User profile management  
**Port:** 3002  
**Technology:** FastAPI + PostgreSQL  
**Features:**
- Biometric data (height, weight, age)
- Fitness goals
- Change history
- Auth Service integration

---

### **3. Plan Management Service** 📋
**Responsible for:** Plan creation & management  
**Port:** 3003  
**Technology:** FastAPI + PostgreSQL  
**Features:**
- CRUD nutrition plans
- User assignment
- Progress tracking
- Event publishing (RabbitMQ)

---

### **4. Nutrition Form Service** 📝
**Responsible for:** Forms & questionnaires  
**Port:** 3004  
**Technology:** FastAPI + PostgreSQL  
**Features:**
- Data collection forms
- Response validation
- Historical storage

---

### **5. Role Permission Service** 🔑
**Responsible for:** Access control (RBAC)  
**Port:** 3005  
**Technology:** FastAPI + PostgreSQL  
**Features:**
- Role management (admin, coach, user)
- Permission assignment
- Access validation
- Authorization middleware

---

### **6. AI Generator Service** 🤖
**Responsible for:** Intelligent plan generation  
**Port:** 3006  
**Technology:** FastAPI + Python ML  
**Features:**
- Personalized plan generation with AI
- Preference analysis
- Smart recommendations
- Async processing

---

### **7. Notification Service** 📢
**Responsible for:** Notification centralization  
**Port:** 3011  
**Technology:** FastAPI + RabbitMQ + MQTT + SMTP  
**Features:**
- RabbitMQ event consumer
- MQTT real-time publisher
- Email delivery (SMTP)
- Smart routing by severity

**Event Flow:**
```
Microservice → RabbitMQ → Notification Svc → MQTT + Email
```

**Documentation:** [services/notification-service/README.md](services/notification-service/README.md)

---

### **8. Notification Dashboard** 📊
**Responsible for:** Real-time notification panel  
**Port:** 3012  
**Technology:** FastAPI + WebSocket  
**Features:**
- Admin dashboard
- Live notifications
- Event history
- System metrics

---

## 💻 Frontend Applications

### **Web App** 🌐
**Location:** `apps/web/`  
**Technologies:** React 19 + TypeScript + Vite + Tailwind CSS  
**Features:**
- Responsive design
- PWA ready
- Hot Module Replacement (HMR)
- ESLint integrated

**Execution:**
```bash
cd apps/web
npm install
npm run dev
```
**Available at:** http://localhost:5173

---

### **Mobile App** 📱
**Location:** `apps/mobile/mobile/`  
**Technologies:** React Native + Expo + TypeScript  
**Features:**
- iOS and Android apps
- Offline synchronization
- Push notifications
- Native modules

**Execution:**
```bash
cd apps/mobile/mobile
npm install
npx expo start
```

---

### **Desktop App** 🖥️
**Location:** `apps/desktop/`  
**Technologies:** Electron + React  
**Features:**
- Advanced offline analysis
- File system integration
- Auto-updates

---

## 📦 Installation and Setup

### **Prerequisites**
```
✅ Docker & Docker Compose v2.0+
✅ Node.js 18+ and npm 10+
✅ Python 3.10+
✅ Git
✅ (Optional) Terraform 1.0+ for AWS deployment
```

### **1. Clone the repository**
```bash
git clone <repo-url>
cd nutrygym-uce
```

### **2. Environment Variables**

Create `.env` files in each service:

```bash
# services/auth-service/.env
DATABASE_URL=postgresql://auth_user:auth_pass@auth-db:5432/auth_db
SECRET_KEY=your-secret-key-here
ALLOWED_DOMAINS=uce.edu.ec

# services/user-profile-service/.env
DATABASE_URL=postgresql://user_user:user_pass@user-db:5432/user_db
AUTH_SERVICE_URL=http://auth-service:3001

# services/notification-service/.env
RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672/
MQTT_HOST=mosquitto
MQTT_PORT=1883
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-app-password
```

### **3. Install Dependencies**

```bash
# Root dependencies (monorepo)
npm install

# Other services are installed within Docker
```

---

## 🚀 Local Execution

### **Option 1: Docker Compose (Recommended)**

```bash
# From project root
docker compose -f docker-compose.global.yml up -d
```

**Available services:**
- 🌐 Web: http://localhost:3000
- 🔐 Auth: http://localhost:3001/docs
- 👤 User Profile: http://localhost:3002/docs
- 📋 Plans: http://localhost:3003/docs
- 📊 Dashboard: http://localhost:3012
- 🌉 Gateway: http://localhost:8080

### **Option 2: Local Development (Frontend + Docker Backend)**

```bash
# Terminal 1: Backend services
docker compose -f docker-compose.global.yml up -d

# Terminal 2: Web app
cd apps/web
npm install
npm run dev

# Terminal 3: (Optional) Mobile
cd apps/mobile/mobile
npx expo start
```

### **Option 3: Full Local Development**

To develop microservices locally:

```bash
# Auth Service
cd services/auth-service
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

---

## 🌐 Deployment on AWS

### **Infrastructure with Terraform**

```bash
cd infrastructure/terraform/envs/qa

# Initialize Terraform
terraform init

# Plan changes
terraform plan

# Apply changes
terraform apply
```

### **Deployed components:**
- EC2 instances (microservices)
- Application Load Balancer (ALB)
- Auto Scaling Groups (ASG)
- RDS PostgreSQL (databases)
- Security Groups
- VPC networking
- Bastion host (secure access)

### **Available environments:**
- **QA:** `infrastructure/terraform/envs/qa/`
- **Production:** `infrastructure/terraform/envs/prod/`

---

## 🔐 Environment Variables

### **Frontend (apps/web)**
```env
VITE_API_URL=http://localhost:8080/api
VITE_MQTT_URL=ws://localhost:8883
```

### **Microservices (services/*)**
```env
# Common
PORT=3001-3012
DATABASE_URL=postgresql://user:pass@host/db
JWT_SECRET=your-secret-key

# Auth Service
ALLOWED_DOMAINS=uce.edu.ec

# Notification Service
RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672/
MQTT_HOST=mosquitto
MQTT_PORT=1883
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASS=app-password
```

---

## 📚 Documentation

### **Service Documentation:**
- [Auth Service](services/auth-service/README.md) - Authentication
- [Notification Service](services/notification-service/README.md) - Notifications
- [Web App](apps/web/README.md) - React Frontend

### **Infrastructure Documentation:**
- [Terraform Modules](infrastructure/terraform/modules/) - IaC

### **API Documentation (Swagger):**
When services are running:
- Auth: http://localhost:3001/docs
- User Profile: http://localhost:3002/docs
- Plans: http://localhost:3003/docs
- etc.

---

## 🧪 Testing & Quality

### **Run tests**
```bash
npm run test
```

### **Run linting**
```bash
npm run lint
```

### **Build for production**
```bash
npm run build
```

### **Load Testing (k6)**
```bash
k6 run ops/load-test/k6-smoke.js
k6 run ops/load-test/k6-basic-load.js
```

---

## 🔄 Development Flow

### **1. Feature Branch**
```bash
git checkout -b feature/new-feature
```

### **2. Develop Locally**
- Use Docker Compose for services
- Turbo for monorepo build/dev
- Automatic hot reload

### **3. Testing**
```bash
npm run test
npm run lint
```

### **4. Build & Deploy**
```bash
npm run build
docker compose -f docker-compose.global.qa.yml up -d
```

### **5. Merge to Main**
- Code review required
- Tests must pass
- Automatic deployment to AWS

---

## 🐛 Troubleshooting

### **Problem: Services can't connect to DB**
```bash
# Check Docker volumes
docker volume ls

# Review logs
docker logs auth-db
```

### **Problem: CORS errors**
```bash
# Check CORS config in each service
# Review gateway (Nginx)
docker logs nutrigym-gateway
```

### **Problem: RabbitMQ connection refused**
```bash
# Wait for RabbitMQ to start
docker logs rabbitmq
# Retry service
docker restart notification-service
```

---

## 📊 Monorepo Architecture (Turbo)

The project uses **Turbo** for optimized builds:

```bash
# Parallel dev
npm run dev

# Build with cache
npm run build

# Lint all packages
npm run lint

# Test all packages
npm run test
```

**Workspaces:**
- `apps/web/`
- `apps/mobile/mobile/`

---

## 🤝 Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This is an academic project of the **Central University of Ecuador (UCE)**.

---

## 📞 Contact & Support

**NutryGym UCE Team**
- 📧 Email: nutrygym.uce@gmail.com
- 🏫 University: Central University of Ecuador
- 📚 Project: Capstone Project

---

## 🎯 Future Roadmap

- [ ] Wearables integration (Apple Watch, Fitbit)
- [ ] Improved Machine Learning for recommendations
- [ ] Predictive health analytics
- [ ] Geolocation integration
- [ ] Multilingual support
- [ ] Security certifications (ISO 27001)
- [ ] Scalability to 1M+ users

---

## 📈 Tech Stack Summary

```
┌─────────────────────────────────────────────────────────────┐
│                    NUTRYGYM UCE STACK                        │
├─────────────────────────────────────────────────────────────┤
│ Frontend  │ React 19 + TypeScript + Vite + Tailwind + Expo  │
├─────────────────────────────────────────────────────────────┤
│ Backend   │ FastAPI + PostgreSQL + RabbitMQ + MQTT + Redis  │
├─────────────────────────────────────────────────────────────┤
│ DevOps    │ Docker + Docker Compose + Terraform + AWS       │
├─────────────────────────────────────────────────────────────┤
│ Tools     │ Turbo + ESLint + Jest + k6 + Swagger            │
└─────────────────────────────────────────────────────────────┘
```

---

**Last Update:** January 2026  
**Version:** 1.0.0
