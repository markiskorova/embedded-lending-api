# Embedded Lending API

A Python-based microservice that simulates an embedded lending platform. Designed for partner platforms to offer simplified merchant loans via REST APIs.

---

## 🗺️ Roadmap

### ✅ Phase 1 – MVP (Core API)
- [ ] Django project and app scaffolding
- [ ] JWT-based merchant authentication
- [ ] Merchant registration/login endpoints
- [ ] Loan application submission API
- [ ] Basic underwriting algorithm (mock scoring)
- [ ] Loan offer generation (amount, interest, duration)
- [ ] Repayment tracking (outstanding balance, payment history)
- [ ] Partner API endpoint to fetch merchant loan offers

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

## 📦 Tech Stack

- **Backend**: Django + DRF
- **Auth**: JWT (SimpleJWT)
- **Database**: PostgreSQL
- **Infrastructure**: Docker, Terraform (AWS)
- **CI/CD**: GitHub Actions
- **Optional**: GraphQL, Celery, Stripe (test mode)

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