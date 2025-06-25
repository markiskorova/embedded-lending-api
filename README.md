# Embedded Lending API

A Python-based backend service that simulates an embedded lending platform. Inspired by real-world embedded lending tools, this project allows merchants to apply for and manage loans through secure REST APIs. The system includes underwriting, loan offers, repayments, and partner-facing APIs.

---

## 📦 Tech Stack

- **Backend**: Django + Django REST Framework (DRF)
- **Auth**: JWT (SimpleJWT)
- **Database**: SQLite (dev), PostgreSQL (prod)
- **Infrastructure**: Docker, Terraform (AWS)
- **CI/CD**: GitHub Actions
- **Optional**: GraphQL (graphene-django), Celery + Redis for background tasks, Prometheus + Grafana (metrics dashboards)

---

## 🗺️ Roadmap

### ✅ Phase 1: Core Lending Workflow MVP
> Simulate the end-to-end lifecycle of a loan through a secure API

- [x] Merchant Registration & JWT Login
- [x] Loan Application Submission
- [x] Basic Underwriting Engine
- [x] Loan Offer Generation
- [x] Offer Acceptance
- [x] Repayment Simulation
- [x] Secure Partner API (Read-Only)

### 🔐 Phase 2: Security, Logging, and Observability
> Add features crucial to trust, compliance, and reliability

- [ ] Field-Level Encryption (Sensitive Data)
- [ ] Decision Logging
- [ ] Request Logging & Audit Trail
- [ ] Enhanced Observability (Prometheus + Grafana dashboards)

### ⚙️ Phase 3: Infrastructure & Extensibility
> Add devops, cloud-readiness, and set up for scalability

- [ ] Dockerized Deployment
- [ ] PostgreSQL Integration (Production Ready)
- [ ] GitHub Actions CI/CD
- [ ] Terraform AWS Provisioning (Optional)

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
