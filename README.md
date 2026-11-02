# Django Clean Architecture API

A structured, scalable, and maintainable RESTful API built with **Django** and **Django REST Framework (DRF)**. This project follows **Clean Architecture** principles to ensure separation of concerns, maintainability, testability, and flexibility.

---

## 🏗️ Architecture

The project is organized into four independent layers:

1. **Domain**: Contains core entities and repository interfaces (abstract classes). This layer has no dependencies on Django or database technologies.
2. **Application**: Contains use cases and business logic. It coordinates application workflows through domain interfaces.
3. **Infrastructure**: Contains Django ORM models and concrete repository implementations responsible for database operations.
4. **Presentation**: Contains API views, serializers, permissions, and URL configurations. It handles HTTP requests and responses.

### Request Flow

```text
HTTP Request
     |
     v
Presentation (Views)
     |
     v
Application (Use Cases)
     |
     v
Domain (Repository Interfaces)
     |
     v
Infrastructure (Repository Implementations)
     |
     v
Database
```

---

## 🚀 Features

- **Clean Architecture**: Separation of business logic, infrastructure, and presentation concerns.
- **Custom User Model**: Extended Django user model with UUID identifiers and additional profile fields.
- **JWT Authentication**: Secure authentication using JSON Web Tokens.
- **User Management**: User registration, profile retrieval, profile updates, and account deletion.
- **Follow System**: Users can follow and unfollow other users.
- **Post Management**: Complete CRUD operations for posts.
- **Ownership Validation**: Users can only modify or delete their own posts.
- **Custom Permissions**: Reusable permission classes to enforce access control.
- **API Documentation**: Interactive API documentation with Swagger UI and ReDoc.
- **Repository Pattern**: Database operations are abstracted behind repository interfaces, making it easier to change data sources or implementations.

---

## 🛠️ Tech Stack

- **Language**: Python 3
- **Framework**: Django
- **REST API**: Django REST Framework
- **Authentication**: djangorestframework-simplejwt
- **Database**: SQLite (Development)
- **API Documentation**: drf-spectacular

## ⚙️ Installation & Setup

Follow these steps to run the project locally.

### 1. Clone the repository

```bash
git clone https://github.com/armin.syntax/drf-clean-architecture.git
cd drf-clean-architecture
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
```

### 3. Activate the virtual environment

**Linux / macOS:**

```bash
source venv/bin/activate
```

**Windows (CMD):**

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Apply database migrations

```bash
python src/manage.py makemigrations
python src/manage.py migrate
```

### 6. Create a superuser (Optional)

```bash
python src/manage.py createsuperuser
```

### 7. Run the development server

```bash
python src/manage.py runserver
```

The API will be available at:

```text
http://127.0.0.1:8000/
```

---

## 📚 API Documentation

This project uses **drf-spectacular** to generate API documentation.

After starting the development server, you can access the documentation through the following endpoints:

| Endpoint | Description |
|---|---|
| `/api/schema/` | OpenAPI schema (JSON/YAML) |
| `/api/docs/` | Swagger UI |
| `/api/redoc/` | ReDoc documentation |

**Documentation URLs:**

- Swagger UI: http://127.0.0.1:8000/api/docs/
- ReDoc: http://127.0.0.1:8000/api/redoc/
- OpenAPI Schema: http://127.0.0.1:8000/api/schema/

---

## 🔐 Authentication

Protected endpoints require a valid JWT access token.

Include the access token in the request headers:

```http
Authorization: Bearer <your_access_token>
```

To obtain a token, send a POST request to:

```text
/api/auth/token/
```

To refresh an expired access token, use:

```text
/api/auth/token/refresh/
```

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Armin Emami**

GitHub: [@armin.syntax](https://github.com/armin.syntax)

---

If you find this project useful, feel free to give it a ⭐ on GitHub!
