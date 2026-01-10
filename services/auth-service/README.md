# 🔐 Auth Service – NutriGym UCE

Authentication microservice for the **NutriGym UCE** platform, developed with **FastAPI**, **PostgreSQL**, and **JWT**, designed under a **microservices architecture** and fully **dockerized**.

This service handles user registration, authentication, and authorization for institutional users of the **Central University of Ecuador (@uce.edu.ec)**.

---

## 🧠 Architecture

- **Framework:** FastAPI (Python)
- **Database:** PostgreSQL 15
- **ORM:** SQLAlchemy
- **Authentication:** JWT (Access & Refresh Tokens)
- **Containers:** Docker & Docker Compose
- **Architecture:** Independent microservice
- **Documentation:** Swagger / OpenAPI

---

## 📂 Project Structure

```text
auth-service/
│
├── app/
│   ├── core/           # Database and security configuration
│   ├── models/         # SQLAlchemy ORM models
│   ├── routes/         # API routes (auth, users)
│   └── services/       # Business logic
│
├── venv/               # Local virtual environment (ignored in Git)
├── __pycache__/        # Python cache files (ignored in Git)
│
├── main.py             # Application entry point
├── init_db.py          # Database initialization script
├── test_db.py          # Database connection tests
│
├── Dockerfile          # Docker image definition
├── docker-compose.yml  # Service orchestration with PostgreSQL
├── requirements.txt   # Python dependencies
├── README.md           # Project documentation
└── .env                # Environment variables (NOT committed)

````

---

## 🐳 Run with Docker (Recommended)

From the `auth-service` directory:

```bash
docker compose up --build
```

The service will be available at:

* 🌐 API: [http://localhost:3001](http://localhost:3001)
* 📚 Swagger: [http://localhost:3001/docs](http://localhost:3001/docs)
* ❤️ Health Check: [http://localhost:3001/health](http://localhost:3001/health)

---

## 🔑 Main Endpoints

### 📌 Authentication

| Method | Endpoint         | Description                |
| ------ | ---------------- | -------------------------- |
| POST   | `/auth/register` | Register new user          |
| POST   | `/auth/login`    | Login and token generation |
| POST   | `/auth/refresh`  | Refresh access token       |
| POST   | `/auth/logout`   | Logout user                |
| GET    | `/auth/me`       | Get authenticated user     |

### 📌 Users

| Method | Endpoint      | Description    |
| ------ | ------------- | -------------- |
| GET    | `/users/`     | List users     |
| GET    | `/users/{id}` | Get user by ID |
| DELETE | `/users/{id}` | Delete user    |

---

## 🔒 Security

* Only institutional emails `@uce.edu.ec` are allowed
* Passwords are encrypted using **bcrypt**
* Signed JWT tokens
* Refresh tokens stored in the database
* CORS configurable per environment

---

## 🧪 Service Status

* ✅ Dockerized
* ✅ Connected to PostgreSQL
* ✅ Health check operational
* ✅ Swagger documentation available
* ✅ Ready for frontend integration (React)

---

## 🚀 Next Steps

* Integration with React frontend
* Route protection for other microservices
* Role-based access control (admin / student)
* API Gateway integration

---

## 👨‍💻 Author

* Juan Tulcanaza
* Developed as part of the **NutriGym UCE** system
* Degree: Information Systems Engineering
* Central University of Ecuador

````
