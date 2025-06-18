# Embedded Lending API

A Python-based backend service that simulates an embedded lending platform. Inspired by real-world tools like Parafin and Stripe Capital, this project allows merchants to apply for and manage loans through secure REST APIs.

---

## 📦 Tech Stack

- **Backend**: Django + Django REST Framework (DRF)
- **Auth**: JWT (SimpleJWT)
- **Database**: SQLite (dev), PostgreSQL (prod)
- **Infrastructure**: Docker, Terraform (AWS)
- **CI/CD**: GitHub Actions
- **Optional**: GraphQL (graphene-django), Celery + Redis for background tasks

---

## 🗺️ Roadmap

### ✅ Phase 1 – MVP (Core API)
- [x] Django project and app scaffolding
- [x] JWT-based merchant authentication
- [x] Merchant registration/login endpoints
- [x] Loan application submission API
- [x] Basic underwriting algorithm (mock scoring)
- [x] Loan offer generation (amount, interest, duration)
- [x] Repayment tracking (outstanding balance, payment history)
- [x] Partner API endpoint to fetch merchant loan offers

### ⚙️ Phase 2 – Infrastructure & DevOps
- [ ] Dockerize the app
- [ ] Add PostgreSQL integration via Docker Compose
- [ ] Use Terraform to deploy to AWS (EC2 + RDS)
- [ ] GitHub Actions for CI/CD

### 🚀 Phase 3 – Enhancements
- [ ] GraphQL API (Strawberry or Graphene)
- [ ] Background risk scoring (Celery or Django-Q)
- [ ] Webhook support with retry & audit logging
- [ ] Simulated Stripe payout/repayment integration
- [ ] Admin dashboard (Django Admin or React)

---

## 🧱 System Architecture (Simplified)

- `users/`: Handles merchant registration and authentication
- `lending/`: Manages loan applications, offers, loans, and repayments
- JWT authentication required for all endpoints
- Partner API endpoint for external systems

---

## 🚧 Getting Started

```bash
# Set up and activate virtualenv
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\Activate.ps1 on Windows

# Install dependencies
pip install -r requirements.txt

# Start project
python manage.py migrate
python manage.py runserver
```
