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
| Python | 3.x |
| Django | 6.0.5 |
| Django REST Framework | 3.17.1 |
| django-cors-headers | 4.9.0 |
| django-filter | 25.2 |
| Pillow | 12.2.0 |
| Database | SQLite (dev) |
| Authentication | Token-based (DRF TokenAuth) |


## API Endpoints

### Auth
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/registration/` | Register a new user |
| POST | `/api/login/` | Login, returns token |
| POST | `/api/logout/` | Logout, invalidates token |

### Profiles
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/profile/` | Get own profile |
| GET/PATCH | `/api/profile/<id>/` | Get or edit profile by ID |
| GET | `/api/profiles/business/` | All business profiles |
| GET | `/api/profiles/customer/` | All customer profiles |

### Offers
| Method | Endpoint | Description |
|---|---|---|
| GET/POST | `/api/offers/` | All offers / create offer |
| GET/PUT/PATCH/DELETE | `/api/offers/<id>/` | Offer by ID |
| GET | `/api/offerdetails/<id>/` | Offer detail (package) by ID |

### Orders
| Method | Endpoint | Description |
|---|---|---|
| GET/POST | `/api/orders/` | All orders / place order |
| GET/PATCH/DELETE | `/api/orders/<id>/` | Order by ID |
| GET | `/api/order-count/<business_user_id>/` | Open orders of a business user |
| GET | `/api/completed-order-count/<business_user_id>/` | Completed orders |

### Reviews
| Method | Endpoint | Description |
|---|---|---|
| GET/POST | `/api/reviews/` | All reviews / submit review |
| GET/PATCH/DELETE | `/api/reviews/<id>/` | Review by ID |

### Base Info
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/base-info/` | Platform statistics |

---

## Installation & Setup

```bash
# 1. Clone repository
git clone https://github.com/croser93/Coderr_BackEnd.git
cd Coderr_BackEnd

# 2. Create and activate virtual environment
python -m venv .venv
source env/bin/activate      # Linux/Mac
env\Scripts\activate         # Windows

# 3. Install dependencies from requirements.txt
pip install -r requirements.txt

# 4. Run database migrations
python manage.py migrate

# 5. Start development server
python manage.py runserver
```

The API is then available at `http://127.0.0.1:8000/api/`.

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
from profile_app.models import ProfileModel

# Customer user
andrey = User.objects.create_user(username='andrey', password='asdasd', email='andrey@test.com')
UserProfile.objects.create(user=andrey, type='customer')
ProfileModel.objects.create(user=andrey, location='Berlin')

# Business user
kevin = User.objects.create_user(username='kevin', password='asdasd24', email='kevin@test.com')
UserProfile.objects.create(user=kevin, type='business')
ProfileModel.objects.create(user=kevin, location='Munich')
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
