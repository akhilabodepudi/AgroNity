# 🌱 AgroNity — Smart Agriculture Platform

AgroNity is a Django-based **digital farming platform** that brings e‑commerce, a soil‑based
crop recommendation engine, nearby agri‑service maps, a learning hub, and a profit/loss
calculator together into a single ecosystem for **farmers, customers, and administrators**.

The goal is to **empower farmers with technology** — not just build another grocery app.

<p align="center">
  <img src="docs/screenshots/01-home.png" alt="AgroNity Home" width="80%">
</p>

---

## Table of Contents

- [Features](#-features )
- [Tech Stack](#-tech-stack)
- [Screenshots](#-screenshots)
  - [Public Pages](#public-pages)
  - [Authentication](#authentication)
  - [Dashboard & Sub-Applications](#dashboard--sub-applications)
  - [Marketplace](#marketplace)
  - [Admin Panel](#admin-panel)
- [Getting Started](#-getting-started)
- [Project Structure](#-project-structure)
- [User Roles](#-user-roles)
- [Roadmap](#-roadmap)
- [References & Inspiration](#-references--inspiration)

---

## ✨ Features

| Module | Description |
| --- | --- |
| 🛒 **Marketplace** | Farmers list crops with price, quantity, quality & images. Customers browse, add to cart, and check out. |
| 🤖 **Crop Recommendation** | An **XGBoost** model suggests the best crop from soil & weather inputs (N, P, K, temperature, humidity, pH, rainfall). |
| 🗺️ **Map Integration** | Find nearby fertilizer shops and soil‑testing centers using OpenStreetMap (Leaflet + Nominatim). |
| 🎓 **Learning Hub** | Curated YouTube tutorials and guides on modern & organic farming practices. |
| 📊 **Profit / Loss Calculator** | Compute net result, profit margin, and ROI from investments and itemized sales. |
| 👥 **Role-Based Accounts** | Custom user model with Farmer, Customer, and Administrator roles (farmers/admins require approval). |
| 🔧 **Admin Panel** | Manage users, crops, cart items, and orders through Django admin. |

---

## 🧰 Tech Stack

- **Backend:** Python 3.11, Django 5.2
- **Machine Learning:** XGBoost, scikit‑learn, NumPy, SciPy, joblib
- **Frontend:** Django Templates, HTML, CSS
- **Maps:** Leaflet.js + OpenStreetMap Nominatim
- **Database:** SQLite (development)
- **Version Control:** Git & GitHub

---

## 📸 Screenshots

### Public Pages

**Home** — landing page with quick access to the dashboard and marketplace.

![Home](docs/screenshots/01-home.png)

### Authentication

| Sign In | Sign Up |
| --- | --- |
| ![Sign in](docs/screenshots/02-sign-in.png) | ![Sign up](docs/screenshots/03-sign-up.png) |

After logging in, the navigation greets the user and exposes role‑based actions.

![Home logged in](docs/screenshots/04-home-logged-in.png)

### Dashboard & Sub-Applications

The **Dashboard** is the launchpad to every sub‑application.

![Dashboard](docs/screenshots/05-dashboard.png)

**Soil Pollution–based Crop Recommendation** — enter soil & weather parameters to get an
ML‑powered crop suggestion.

![Crop Recommendation](docs/screenshots/06-crop-recommendation.png)

**Map Integration** — locate nearby fertilizer shops and soil test centers.

![Map Integration](docs/screenshots/07-map-integration.png)

**Learning Hub** — embedded farming tutorials.

![Learning Hub](docs/screenshots/08-learning-hub.png)

**Profit / Loss Calculator** — net result, profit margin, and ROI at a glance.

![Profit / Loss](docs/screenshots/09-profit-loss.png)

### Marketplace

| Open Market | Cart | Payment (Demo) |
| --- | --- | --- |
| ![Market](docs/screenshots/10-market.png) | ![Cart](docs/screenshots/11-cart.png) | ![Payment](docs/screenshots/12-payment.png) |

### Admin Panel

| Site Administration | Users | Crops |
| --- | --- | --- |
| ![Admin home](docs/screenshots/14-admin-home.png) | ![Admin users](docs/screenshots/13-admin-users.png) | ![Admin crops](docs/screenshots/17-admin-crops.png) |

Editing a user — including AgroNity‑specific fields such as **Role** and **Is approved**:

| Change user | Permissions & role |
| --- | --- |
| ![Admin user edit](docs/screenshots/15-admin-user-edit.png) | ![Admin user permissions](docs/screenshots/16-admin-user-permissions.png) |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- `pip` and `venv`

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/akhilabodepudi/AgroNity.git
cd AgroNity

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply database migrations
python manage.py migrate

# 5. Create an admin account
python manage.py createsuperuser

# 6. Run the development server
python manage.py runserver
```

Then open:

- App: <http://127.0.0.1:8000/>
- Marketplace: <http://127.0.0.1:8000/market/>
- Admin: <http://127.0.0.1:8000/admin/>

> The crop recommendation model is loaded from `ml_model/xgboost.pkl` at runtime.

---

## 🗂️ Project Structure

```text
agronity/
├── core/                 # Django project settings, root URLs, WSGI/ASGI
├── accounts/             # Custom User model, auth views (home, login, signup, logout)
├── market/               # Marketplace, cart, checkout, recommendation, maps, learning, profit/loss
├── ml_model/             # Trained XGBoost crop-recommendation model (xgboost.pkl)
├── templates/            # Global + app templates (base.html, dashboard, subapps, market, accounts)
├── static/               # Static assets (CSS/JS/img)
├── media/                # User-uploaded files (crop images)
├── docs/screenshots/     # README screenshots
├── manage.py
└── requirements.txt
```

---

## 👥 User Roles

| Role | Capabilities |
| --- | --- |
| **Farmer** | Register/login, manage profile, list and manage crops, view orders *(requires admin approval)*. |
| **Customer** | Register/login, browse crops, add to cart, and place orders *(auto‑approved)*. |
| **Administrator** | Manage farmers, customers, crops, cart items, and orders from the admin panel *(requires approval)*. |

---

## 🛣️ Roadmap

- [ ] Expand the crop dataset (more regions, soil types, weather integration)
- [ ] Leaf disease detection using image‑based ML
- [ ] Fertilizer recommendation based on crop & soil data
- [ ] Real payment gateway integration
- [ ] Local language support and improved UI/UX
- [ ] Native Android / iOS apps

---

## 📚 References & Inspiration

- Government of India agriculture portals (mKisan, Kisan Suvidha, AgriStack)
- Digital farming platforms: OneSoil, Climate FieldView, CropX, Agricolus
- Research on soil‑based crop recommendation using machine learning
- YouTube channels & tutorials on organic and modern agricultural practices

---

<p align="center"><em>AgroNity — uniting farmers, buyers, and knowledge into one ecosystem. 🌾</em></p>
