# Plan Management Service

## Overview
The Plan Management Service is a core microservice of the **NutriGym Platform**.

It is responsible for managing personalized meal plans for users and orchestrating AI-based plan generation, while emitting system events for observability and notifications.

---

## Responsibilities
- Create and update personalized meal plans
- Maintain the current active plan per user
- Version and regenerate plans
- Orchestrate AI-based plan generation
- Publish plan lifecycle events to RabbitMQ

---

## Technologies
- **FastAPI**
- **PostgreSQL**
- **Redis**
- **RabbitMQ**
- **JWT Authentication**
- **Docker**
- **OpenAPI (Swagger)**

---

## Event-Driven Integration
This service publishes **notification events** to **RabbitMQ** on key actions:

- Plan generated
- Plan regenerated
- Plan ended
- Plan canceled
- Plan generation errors

Events are published to:

````

notifications.queue

````

These events are later:
- Consumed by the **Notification Service**
- Broadcast via **MQTT**
- Optionally delivered via **Email**

> ⚠️ This service does **not** send emails directly.

---

## Authentication
All external endpoints are protected using **JWT Bearer tokens** issued by the Auth Service.

---

## API Endpoints

| Method | Endpoint | Description |
|------|---------|------------|
| GET | `/plans` | Get all user plans |
| POST | `/plans` | Create a plan |
| GET | `/plans/current` | Get active plan |
| POST | `/plans/generate` | Generate plan using AI |
| POST | `/plans/current/regenerate` | Regenerate active plan |
| POST | `/plans/current/end` | End active plan |
| POST | `/plans/current/cancel` | Cancel active plan |
| GET | `/health` | Health check |

---

## Environment Variables

```env
PORT=3005

DATABASE_URL=postgresql://user:password@plan-postgres:5432/nutrigym_plans

JWT_SECRET=your_jwt_secret
JWT_ALGORITHM=HS256

RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672/
NOTIF_QUEUE=notifications.queue
````

---

## Architecture Role

* **Domain:** Core Business
* **Consumes:** Auth Service, User Profile, Nutrition Form, AI Generator
* **Produces:** Meal Plans + Notification Events
* **Pattern:** Event-driven core service

---

## Status

✅ Stable
🚀 Integrated with Notification & Dashboard Services

---

## 👨‍💻 Author

**Juan Tulcanaza**
Information Systems Engineering
Central University of Ecuador
Developed as part of the **NutriGym UCE Platform**

