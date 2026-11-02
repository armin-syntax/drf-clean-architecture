# Django Clean Architecture API

A scalable RESTful API built with **Django** and **Django REST Framework (DRF)**, following **Clean Architecture** principles.

The project demonstrates a modular backend architecture with independent business logic, JWT authentication, multi-database integration, and data synchronization. It is fully containerized using Docker Compose.

## Tech Stack

- **Language:** Python 3
- **Backend:** Django, Django REST Framework
- **Databases:** PostgreSQL, SQLite
- **Authentication:** JWT (Simple JWT)
- **API Documentation:** drf-spectacular
- **Containerization:** Docker, Docker Compose

## Architecture

The application is organized into four layers:

- **Domain:** Core entities and repository interfaces.
- **Application:** Use cases and business logic.
- **Infrastructure:** Database models and repository implementations.
- **Presentation:** API views, serializers, and permissions.

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/armin-syntax/drf-clean-architecture.git
cd drf-clean-architecture
```

### 2. Build and start the containers

```bash
docker compose up --build -d
```

### 3. Populate the external SQLite database

```bash
docker compose exec web python seed_external.py
```

### 4. Apply database migrations

```bash
docker compose exec web python manage.py migrate
```

### 5. Create a superuser

```bash
docker compose exec web python manage.py createsuperuser
```

### 6. Access the application

The API will be available at:

http://127.0.0.1:8000/

## Data Synchronization

The project includes an admin-only endpoint for synchronizing users from the external SQLite database into the primary PostgreSQL database.

```http
POST /api/users/sync/
```

Only administrators can access this endpoint.

## API Documentation

Once the containers are running, access the interactive API documentation:

- **Swagger UI:** http://127.0.0.1:8000/api/docs/
- **ReDoc:** http://127.0.0.1:8000/api/redoc/
- **OpenAPI Schema:** http://127.0.0.1:8000/api/schema/

## Stopping the Application

```bash
docker compose down
```

To remove containers and volumes:

```bash
docker compose down -v
```

**Note:** Removing volumes may permanently delete database data.

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

**Author:** [Armin](https://github.com/armin-syntax)
