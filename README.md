# Coderr Backend

This project is the **Django REST Framework backend** for the existing frontend application [Coderr FrontEnd](https://github.com/croser93/Coder_FrontEnd.git).

> **Developer Akademie learning project** — The backend was independently developed to fully connect to the given frontend and implement all core platform features.

---

## About the Project

Coderr is a platform where **business users** can list their services as offers and **customers** can order and review those offers. The backend provides a REST API that fully serves the existing frontend.

---

## Tech Stack

| Technology | Version |
|---|---|
| Python | 3.14.4 |
| Django | 6.0.5 |
| Django REST Framework | 3.17.1 |
| django-cors-headers | 4.9.0 |
| django-filter | 25.2 |
| Pillow | 12.2.0 |
| Database | SQLite (dev) |
| Authentication | Token-based (DRF TokenAuth) |


---

## Installation & Setup

```bash
# 1. Clone repository
git clone https://github.com/croser93/Coderr_BackEnd.git
```
```bash
# 2. go to Projekt
cd Coderr_BackEnd
```

```bash
# 3. Create and activate virtual environment
python -m venv .venv
```

```bash
# 4.Activate the virtual environment only Linux/Mac!
source env/bin/activate
```

```bash
# 4.Activate the virtual environment only Windows!
env\Scripts\activate
```

```bash
# 5. Install dependencies from requirements.txt
pip install -r requirements.txt
```

```bash
# 6. Creates migration files
python manage.py makemigrations
```

```bash
# 7. Run database migrations
python manage.py migrate
```

```bash
# 8. Start development server
python manage.py runserver
```
---

## Demo Users

To use the platform right away, you can create two demo users via the Django shell.

**Important:** Each user needs entries in both `auth_app` (type) and `profile_app` (profile), otherwise the API will not work correctly.

```bash
python manage.py shell
```

Then paste the following block into the shell:

```python
from django.contrib.auth.models import User
from auth_app.models import UserProfile
from profile_app.models import Profiles

andrey = User.objects.create_user(username='andrey', password='asdasd', email='andrey@test.com', first_name='Andrey', last_name='Customer')
UserProfile.objects.create(user=andrey, type='customer')
Profiles.objects.create(user=andrey, location='Berlin')

kevin = User.objects.create_user(username='kevin', password='asdasd24', email='kevin@test.com', first_name='Kevin', last_name='Business')
UserProfile.objects.create(user=kevin, type='business')
Profiles.objects.create(user=kevin, location='Munich')
```

| Role | Username | Password |
|---|---|---|
| Customer | `andrey` | `asdasd` |
| Business | `kevin` | `asdasd24` |

---

## Project Structure

```
Coderr_BackEnd/
├── core/               # Project configuration (settings, urls, wsgi)
├── auth_app/           # Registration, login, logout
├── profile_app/        # User profiles (business & customer)
├── offers_app/         # Offers and offer packages
├── orders_app/         # Order management
├── reviews_app/        # Review system
└── baseinfo_app/       # Platform statistics
```

---

## Frontend

The corresponding frontend can be found here:
[https://github.com/croser93/Coder_FrontEnd.git](https://github.com/croser93/Coder_FrontEnd.git)

---

## Author

**Maik G.** — Learning project as part of the [Developer Akademie](https://developerakademie.com/)
