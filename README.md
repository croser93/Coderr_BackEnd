# Coderr Backend

Dieses Projekt ist das **Django REST Framework Backend** zur bestehenden Frontend-Anwendung [Coderr FrontEnd](https://github.com/croser93/Coder_FrontEnd.git).

> **Lernprojekt der Developer Akademie** — Das Backend wurde eigenständig entwickelt, um das vorgegebene Frontend vollständig anzubinden und damit alle Kernfunktionen der Plattform zu realisieren.

---

## Über das Projekt

Coderr ist eine Plattform, auf der **Business-User** ihre Dienstleistungen als Angebote einstellen und **Kunden** diese Angebote bestellen und bewerten können. Das Backend stellt eine REST API bereit, die das bestehende Frontend vollständig versorgt.

---

## Tech Stack

| Technologie | Version |
|---|---|
| Python | 3.x |
| Django | 6.0 |
| Django REST Framework | latest |
| django-cors-headers | latest |
| django-filter | latest |
| Datenbank | SQLite (dev) |
| Authentifizierung | Token-basiert (DRF TokenAuth) |

---

## Features

- **Authentifizierung** — Registrierung, Login, Logout mit Token-Authentifizierung
- **Profile** — Nutzerprofile für Business- und Customer-User
- **Angebote** — Angebote erstellen, abrufen, bearbeiten und löschen (inkl. Detailpakete: Basic, Standard, Premium)
- **Bestellungen** — Bestellungen aufgeben, Status verwalten (`in_progress`, `completed`, `cancelled`)
- **Bewertungen** — Bewertungen zu Business-Usern abgeben und abrufen
- **Base-Info** — Aggregierte Plattformstatistiken

---

## API Endpunkte

### Auth
| Methode | Endpunkt | Beschreibung |
|---|---|---|
| POST | `/api/registration/` | Neuen Nutzer registrieren |
| POST | `/api/login/` | Login, gibt Token zurück |
| POST | `/api/logout/` | Logout, invalidiert Token |

### Profile
| Methode | Endpunkt | Beschreibung |
|---|---|---|
| GET | `/api/profile/` | Eigenes Profil abrufen |
| GET/PATCH | `/api/profile/<id>/` | Profil nach ID abrufen/bearbeiten |
| GET | `/api/profiles/business/` | Alle Business-Profile |
| GET | `/api/profiles/customer/` | Alle Customer-Profile |

### Angebote
| Methode | Endpunkt | Beschreibung |
|---|---|---|
| GET/POST | `/api/offers/` | Alle Angebote / Angebot erstellen |
| GET/PUT/PATCH/DELETE | `/api/offers/<id>/` | Angebot nach ID |
| GET | `/api/offersdetails/<id>/` | Angebotsdetail (Paket) nach ID |

### Bestellungen
| Methode | Endpunkt | Beschreibung |
|---|---|---|
| GET/POST | `/api/orders/` | Alle Bestellungen / Bestellung aufgeben |
| GET/PATCH/DELETE | `/api/orders/<id>/` | Bestellung nach ID |
| GET | `/api/order-count/<business_user_id>/` | Offene Bestellungen eines Business-Users |
| GET | `/api/completed-order-count/<business_user_id>/` | Abgeschlossene Bestellungen |

### Bewertungen
| Methode | Endpunkt | Beschreibung |
|---|---|---|
| GET/POST | `/api/reviews/` | Alle Bewertungen / Bewertung abgeben |
| GET/PATCH/DELETE | `/api/reviews/<id>/` | Bewertung nach ID |

### Base Info
| Methode | Endpunkt | Beschreibung |
|---|---|---|
| GET | `/api/base-info/` | Plattformstatistiken |

---

## Installation & Setup

```bash
# 1. Repository klonen
git clone https://github.com/croser93/Coderr_BackEnd.git
cd Coderr_BackEnd

# 2. Virtuelle Umgebung erstellen und aktivieren
python -m venv env
source env/bin/activate      # Linux/Mac
env\Scripts\activate         # Windows

# 3. Abhängigkeiten installieren
pip install django djangorestframework django-cors-headers django-filter pillow

# 4. Datenbank migrieren
python manage.py migrate

# 5. Entwicklungsserver starten
python manage.py runserver
```

Die API ist anschließend unter `http://127.0.0.1:8000/api/` erreichbar.

---

## Projektstruktur

```
Coderr_BackEnd/
├── core/               # Projektkonfiguration (settings, urls, wsgi)
├── auth_app/           # Registrierung, Login, Logout
├── profile_app/        # Nutzerprofile (Business & Customer)
├── offers_app/         # Angebote und Angebotspakete
├── orders_app/         # Bestellverwaltung
├── reviews_app/        # Bewertungssystem
└── baseinfo_app/       # Plattformstatistiken
```

---

## Frontend

Das zugehörige Frontend findet sich hier:
[https://github.com/croser93/Coder_FrontEnd.git](https://github.com/croser93/Coder_FrontEnd.git)

---

## Autor

**Maik G.** — Lernprojekt im Rahmen der [Developer Akademie](https://developerakademie.com/)
