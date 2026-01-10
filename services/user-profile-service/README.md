# 🧍 User Profile Service – NutriGym

## 📌 Overview

The **User Profile Service** is a core backend microservice of the **NutriGym platform**, responsible for managing users’ personal and physical information required for nutritional analysis and personalized plan generation.

This service stores and exposes structured profile data such as name, birth date, gender, height, weight, fitness goals, and activity level. It follows a **microservices-based architecture**, operates independently, and integrates securely with the Authentication Service using **JWT-based authorization**.

---

## 🎯 Responsibilities

* Create and manage user profile information
* Associate profile data with authenticated users
* Expose profile data to other backend services
* Enforce access control using JWT authentication
* Persist structured profile data in PostgreSQL

---

## 🧩 Service Scope

This service **does NOT handle**:

* Authentication or login (handled by `auth-service`)
* Role or permission management
* Nutritional plan generation logic

The service strictly focuses on the **user profile domain**, ensuring a clear separation of concerns and maintainable service boundaries.

---

## 🛠️ Tech Stack

* **Backend Framework:** FastAPI (Python)
* **Database:** PostgreSQL
* **ORM:** SQLAlchemy
* **Authentication:** JWT (validated via Authorization header)
* **Containerization:** Docker & Docker Compose
* **API Documentation:** OpenAPI / Swagger UI

---

## 📂 Project Structure

```
user-profile-service/
├── app/
│   ├── core/
│   │   ├── database.py
│   │   └── security.py
│   ├── models/
│   │   └── user_profile.py
│   ├── routes/
│   │   └── profiles.py
│   ├── schemas/
│   │   └── profile.py
│   └── services/
│       └── profile_service.py
├── main.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

## 🔐 Authentication & Security

All protected endpoints require a **valid JWT token** issued by the `auth-service`.

The token must be included in the request header:

```
Authorization: Bearer <JWT_TOKEN>
```

The `user_id` is extracted from the JWT `sub` claim and is used internally to associate profile records with the authenticated user.

---

## 📡 API Endpoints

### 🔹 Create User Profile

**POST** `/profiles`

Creates a profile for the authenticated user.

**Request Body:**

```json
{
  "first_name": "Juan",
  "last_name": "Pérez",
  "birth_date": "1995-05-15",
  "gender": "male",
  "height_cm": 180,
  "weight_kg": 75.5,
  "goal": "muscle_gain",
  "activity_level": "moderate"
}
```

**Response (200 OK):**

```json
{
  "id": "uuid",
  "user_id": "uuid",
  "first_name": "Juan",
  "last_name": "Pérez",
  "birth_date": "1995-05-15",
  "gender": "male",
  "height_cm": 180,
  "weight_kg": 75.5,
  "goal": "muscle_gain",
  "activity_level": "moderate"
}
```

---

### 🔹 Get My Profile

**GET** `/profiles/me`

Returns the profile associated with the authenticated user.

---

### 🔹 Health Check

**GET** `/health`

Returns the current health status of the service and database connectivity.

---

## 🧪 API Documentation

Once the service is running, interactive API documentation is available at:

```
http://localhost:3002/docs
```

---

## 🐳 Running with Docker

### 1️⃣ Start the Service

```bash
docker compose up --build
```

The service will be available at:

```
http://localhost:3002
```

---

## 🔗 Service Integration

This microservice integrates with the following components of the NutriGym system:

* **Auth Service** → JWT validation and user identity
* **Nutrition Form Service** → Profile data for nutritional calculations
* **Plan Management Service** → Personalization of nutrition plans
* **AI Generator Service** → Contextual data for AI-driven recommendations

Communication is currently **synchronous (REST-based)**. Asynchronous integration via Kafka or RabbitMQ can be introduced in future iterations.

---

## 📈 Scalability & Architecture Notes

* Stateless microservice (supports horizontal scaling)
* Independent database for fault isolation
* Fully Dockerized and cloud-ready
* Compatible with API Gateway routing
* Designed to integrate with CI/CD pipelines

---

## 👨‍💻 Author

* **Juan Tulcanaza**
* Developed as part of the **NutriGym UCE** system
* Degree Program: **Information Systems Engineering**
* Institution: **Central University of Ecuador**
