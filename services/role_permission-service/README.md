# 🔐 Authorization Service – NutriGym

## 📌 Overview

The **Authorization Service** is a core security microservice of the **NutriGym platform**, responsible for validating user access based on predefined roles.

This service does **not manage users, roles, or authentication**. Instead, it validates **JWT tokens issued by the Authentication Service** and determines whether a user is allowed to access a specific resource or screen.

The platform operates with **two fixed roles only**:

* **ADMIN** → Access to administrative dashboards and management features
* **ESTUDIANTE** → Access to personal profile, nutrition data, and meal plan generation

---

## 🎯 Responsibilities

* Validate JWT tokens issued by `auth-service`
* Extract user identity and role from the token
* Enforce role-based access control (RBAC)
* Determine whether access is granted or denied
* Provide authorization decisions to other services or the frontend

---

## 🚫 Out of Scope

This service **does NOT handle**:

* User registration or login
* Role creation or modification
* Role assignment logic
* Database persistence
* Nutrition or business logic

Its sole responsibility is **authorization**.

---

## 🛠️ Tech Stack

* **Backend Framework:** FastAPI (Python)
* **Security:** JWT (HS256)
* **Authorization Model:** Role-Based Access Control (RBAC)
* **Containerization:** Docker & Docker Compose
* **API Documentation:** OpenAPI (Swagger)

---

## 📂 Project Structure

```
role_permission-service/
├── app/
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   └── routes/
│       └── authorization.py
├── main.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env
└── README.md
```

---

## 🔐 Authentication & Authorization

All protected endpoints require a **valid JWT token** issued by the `auth-service`.

The token must include the following claims:

```json
{
  "sub": "user_uuid",
  "email": "user@uce.edu.ec",
  "role": "ADMIN | ESTUDIANTE",
  "exp": 1768044576
}
```

### Required Header

```
Authorization: Bearer <JWT_TOKEN>
```

⚠️ The `JWT_SECRET_KEY` **must be exactly the same** as the one used in `auth-service`.

---

## 📡 API Endpoints

### 🔹 Check Access

**GET** `/authorize/check`

Validates whether the authenticated user has the required role.

**Query Parameters:**

* `required_role` → `ADMIN` or `ESTUDIANTE`

**Example Request:**

```http
GET /authorize/check?required_role=ESTUDIANTE
Authorization: Bearer <JWT_TOKEN>
```

**Successful Response (200 OK):**

```json
{
  "user_id": "uuid",
  "email": "user@uce.edu.ec",
  "user_role": "ESTUDIANTE",
  "required_role": "ESTUDIANTE",
  "allowed": true,
  "message": "✅ Access granted"
}
```

**Access Denied Example:**

```json
{
  "user_id": "uuid",
  "email": "admin@uce.edu.ec",
  "user_role": "ADMIN",
  "required_role": "ESTUDIANTE",
  "allowed": false,
  "message": "❌ Access denied. Your role: ADMIN"
}
```

---

### 🔹 Get My Role

**GET** `/authorize/my-role`

Returns the role associated with the authenticated user.

---

### 🔹 Health Check

**GET** `/health`

Returns the service health status.

---

## 🧪 API Documentation

Interactive Swagger documentation is available at:

```
http://localhost:3003/docs
```

---

## 🐳 Running with Docker

### 1️⃣ Start the Service

```bash
docker compose up --build
```

Service will be available at:

```
http://localhost:3003
```

---

## 🔗 Service Integration

This service integrates with:

* **Auth Service** → JWT issuance and identity
* **Frontend (React)** → Route protection and screen access
* **API Gateway** → Centralized authorization checks
* **Other Microservices** → Access validation

Communication is **synchronous (REST)**.

---

## 📈 Architecture Notes

* Stateless and horizontally scalable
* No database dependency
* Cloud-native and Docker-ready
* Ideal for API Gateway enforcement
* Clear separation of concerns

---

## 👨‍💻 Author

* **Juan Tulcanaza**
* Developed as part of the **NutriGym UCE** platform
* Degree: Information Systems Engineering
* Central University of Ecuador

