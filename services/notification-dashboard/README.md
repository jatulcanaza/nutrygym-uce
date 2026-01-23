# Notification Dashboard Service

## Overview
The Notification Dashboard Service provides a **real-time visualization layer** for system notifications.

It allows developers and administrators to observe system events as they occur, without directly accessing message brokers.

---

## Responsibilities
- Subscribe to MQTT topics
- Receive real-time notification messages
- Stream notifications to the browser using WebSockets
- Provide a lightweight monitoring dashboard

---

## Technologies
- **FastAPI**
- **WebSockets**
- **MQTT (paho-mqtt)**
- **Docker**
- **HTML / JavaScript**

---

## Architecture Role
- **Domain:** Observability / Monitoring
- **Consumes:** MQTT messages (`nutrygym/notifications`)
- **Exposes:** Web UI + WebSocket stream
- **Pattern:** Real-time pub/sub

---

## How It Works
1. The service connects to the MQTT broker
2. Subscribes to the notification topic
3. Forwards messages to connected WebSocket clients
4. Messages are displayed instantly in the browser

---

## Access
Once running, open:

````

[http://localhost:3012](http://localhost:3012)

```

The dashboard automatically connects to:
```

ws://localhost:3012/ws

````

---

## Environment Variables
```env
PORT=3012

MQTT_HOST=mosquitto
MQTT_PORT=1883
MQTT_TOPIC=nutrygym/notifications
````

---

## Status

✅ Stable
📡 Real-time MQTT streaming enabled

---

## 👨‍💻 Author

**Juan Tulcanaza**
Information Systems Engineering
Central University of Ecuador
Developed as part of the **NutriGym UCE Platform**