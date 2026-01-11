# Plan Management Service

## Overview
The Plan Management Service is a core microservice of the NutriGym platform.  
It is responsible for creating, updating, versioning, and managing personalized meal plans for users.

This service represents the **core business logic** of the system and operates independently from authentication and user profile management.

---

## Responsibilities
- Create personalized meal plans
- Update and version existing plans
- Associate plans with authenticated users
- Maintain historical records of meal plans
- Expose secure REST APIs for plan management

---

## Technologies
- **FastAPI**
- **PostgreSQL**
- **JWT Authentication**
- **Docker**
- **OpenAPI (Swagger)**

---

## Authentication
All endpoints are protected using **JWT Bearer tokens** issued by the Auth Service.

The service validates:
- User identity (`sub`)
- Token integrity
- Token expiration

---

## API Endpoints
| Method | Endpoint | Description |
|------|---------|------------|
| GET | `/plans` | Get all plans of the authenticated user |
| POST | `/plans` | Create a new meal plan |
| GET | `/plans/{plan_id}` | Get a specific plan |
| PUT | `/plans/{plan_id}` | Update an existing plan |
| DELETE | `/plans/{plan_id}` | Delete a plan |
| GET | `/plans/current` | Get current active plan |
| GET | `/health` | Service health check |

---

## Environment Variables
The service is configured via a `.env` file:

```env
PORT=3005
DATABASE_URL=postgresql://user:password@postgres:5432/nutrigym_plans
JWT_SECRET=your_jwt_secret
JWT_ALGORITHM=HS256
````

---

## Architecture Role

* **Domain:** Core System
* **Consumes:** Authentication tokens
* **Produces:** Structured meal plan data
* **Future integrations:** AI Generator, Event Streaming (Kafka)

---

## Status

✅ Stable
🚀 Ready for integration with Nutrition Form and AI Generator services

---
```
## 👨‍💻 Author

**Juan Tulcanaza**
Information Systems Engineering
Central University of Ecuador
Developed as part of the **NutriGym UCE Platform**


