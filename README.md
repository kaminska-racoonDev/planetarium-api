# Planetarium API 🪐

A RESTful API for managing a planetarium — astronomy shows, show sessions, dome reservations, and ticketing. Built with Django REST Framework and JWT authentication.

---

## Features

- Astronomy Shows — create and manage shows with multiple themes
- Show Themes — tag shows with reusable themes (e.g. "Space", "Science")
- Planetarium Domes — manage domes with rows and seat capacity
- Show Sessions — schedule shows in specific domes at specific times
- Reservations — authenticated users can make and view their own reservations
- Tickets — assign seats (row + seat number) to reservations for a session
- Available Seats — automatically calculated per session based on dome capacity
- Filtering — filter shows and sessions by title and theme; filter domes by name
- JWT Authentication — secure access with access and refresh tokens
- Swagger UI — interactive API documentation at `/api/v1/doc/`
- Admin panel — manage all data via Django admin at `/admin/`

---

## Tech Stack

- Python 3
- Django 6
- Django REST Framework
- Simple JWT
- drf-spectacular (Swagger)
- SQLite (default)

---

## Running Locally

### 1. Clone the repository

```bash
git clone https://github.com/your-username/planetarium-api.git
cd planetarium-api
```

### 2. Create and activate a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. (Optional) Load sample data

```bash
python manage.py loaddata planetarium_fixture.json
```

### 6. Create a superuser

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

---

## Getting Access

### Register a new account

```
POST /api/v1/user/register/
```

```json
{
    "email": "your@email.com",
    "password": "yourpassword"
}
```

### Log in to get tokens

```
POST /api/v1/user/login/
```

```json
{
    "email": "your@email.com",
    "password": "yourpassword"
}
```

You'll receive an `access` token and a `refresh` token:

```json
{
    "access": "eyJ...",
    "refresh": "eyJ..."
}
```

### Use the access token

Include it in the `Authorization` header for all authenticated requests:

```
Authorization: Bearer <your_access_token>
```

### Refresh your token

Access tokens expire after 30 minutes. Use the refresh token to get a new one:

```
POST /api/v1/user/token/refresh/
```

```json
{
    "refresh": "eyJ..."
}
```

---


### Filtering

| Endpoint | Filter params |
|---|---|
| `/astronomy_show/` | `?title=mars` `?themes=1,2` |
| `/show_session/` | `?title=mars` `?themes=1` `?show_time=2025-08-01` |
| `/planetarium_dome/` | `?name=main` |

---

## API Documentation

Interactive Swagger UI is available at:

```
http://127.0.0.1:8000/api/v1/doc/swagger/
```

---

## Running Tests

```bash
python manage.py test
```