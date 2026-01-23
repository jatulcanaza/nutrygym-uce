# Notification Service

## Overview
The Notification Service is a communication microservice within the **NutriGym Platform**.

Its responsibility is to **centralize system notifications**, decouple them from business logic, and distribute them through multiple channels such as **real-time dashboards (MQTT)** and **email (SMTP)**.

This service acts as an **event consumer and dispatcher**, isolating notification concerns from core services.

---

## Responsibilities
- Consume notification events from **RabbitMQ**
- Normalize and process notification payloads
- Publish real-time notifications to **MQTT topics**
- Send email notifications via **SMTP (Gmail)**
- Route notifications to **users or administrators** based on severity and configuration

---

## Technologies
- **FastAPI**
- **RabbitMQ**
- **MQTT (Mosquitto)**
- **SMTP (Gmail App Password)**
- **Docker**
- **Python**

---

## Architecture Role
- **Domain:** Communication / Notifications
- **Consumes:** RabbitMQ events (`notifications.queue`)
- **Publishes:** MQTT messages (`nutrygym/notifications`)
- **Sends:** Email alerts (Admin / Users)
- **Pattern:** Event-driven, asynchronous, decoupled

---

## Event Flow
1. A backend service (e.g. Plan Management) publishes an event to RabbitMQ
2. Notification Service consumes the event
3. The event is:
   - Broadcast via MQTT (real-time dashboard)
   - Optionally sent via email (admin or user)
4. Dashboards and email clients receive the notification

---

## Email Routing Rules
The email behavior is fully configurable:

### User Emails
- Sent **only if** the event contains an `email` field
- Controlled by:
```env
SEND_USER_EMAILS=true
````

### Admin Alerts

* Sent when:

  * `event.email` is **not present**
  * `event.severity` matches configured levels
* Controlled by:

```env
ADMIN_EMAIL=nutrygym.uce@gmail.com
SEND_ADMIN_ALERTS=true
ADMIN_ALERT_SEVERITIES=info,warning,error
```

---

## Environment Variables

Configured via `.env`:

```env
PORT=3011

# RabbitMQ
RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672/
RABBITMQ_QUEUE=notifications.queue
RABBITMQ_PREFETCH=20

# MQTT
MQTT_HOST=mosquitto
MQTT_PORT=1883
MQTT_TOPIC=nutrygym/notifications

# SMTP (Gmail)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=nutrygym.uce@gmail.com
SMTP_PASS=app_password_here
SMTP_FROM=nutrygym.uce@gmail.com
SMTP_USE_TLS=true

# Email routing
ADMIN_EMAIL=nutrygym.uce@gmail.com
SEND_USER_EMAILS=true
SEND_ADMIN_ALERTS=true
ADMIN_ALERT_SEVERITIES=info,warning,error
```

---

## API Endpoints

| Method | Endpoint  | Description  |
| ------ | --------- | ------------ |
| GET    | `/health` | Health check |

> This service does **not** expose business APIs.
> All communication is asynchronous and event-driven.

---

## Status

✅ Stable
📧 Email notifications enabled
📡 Real-time MQTT broadcasting enabled

---

## 👨‍💻 Author

**Juan Tulcanaza**
Information Systems Engineering
Central University of Ecuador
Developed as part of the **NutriGym UCE Platform**
