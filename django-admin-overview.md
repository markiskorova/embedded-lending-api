# Django Admin for Embedded Lending API — Why, What, and How

## Why Add Django Admin
- **Instant internal console:** Manage merchants, loan applications, offers, disbursements, and repayments without building custom dashboards.
- **Productivity boost:** Search, filter, edit, and review data in minutes—useful for Ops, Support, and QA.
- **Single source of truth:** Works directly off your Django models, so fields and validations stay consistent.
- **Auditability & control:** Built-in change history (LogEntry) and role-based access via Django auth.
- **Low effort, high leverage:** A few lines of config + model registration = a powerful back office.

## Basic Functionality (At a Glance)
- **CRUD UI for models:** Create, read, update, and delete records with validations.
- **Search & filters:** Configure which fields are searchable or filterable (e.g., status, merchant).
- **Inlines & relations:** Display related objects (e.g., Offers/Repayments inside a LoanApplication view).
- **Permissions:** Restrict access by user/group; make models or fields read-only.
- **Bulk actions:** Custom actions (e.g., “Approve selected applications”).

## Implementation Plan (Step-by-Step)
1. **Enable Admin apps (settings.py)**
   ```python
   INSTALLED_APPS = [
       "django.contrib.admin",
       "django.contrib.auth",
       "django.contrib.contenttypes",
       "django.contrib.sessions",
       "django.contrib.messages",
       "django.contrib.staticfiles",
       # your apps
       "users",
       "lending",
   ]
   MIDDLEWARE = [
       "django.middleware.security.SecurityMiddleware",
       "django.contrib.sessions.middleware.SessionMiddleware",
       "django.middleware.common.CommonMiddleware",
       "django.middleware.csrf.CsrfViewMiddleware",
       "django.contrib.auth.middleware.AuthenticationMiddleware",
       "django.contrib.messages.middleware.MessageMiddleware",
   ]
   ```

2. **Wire the URL (urls.py)**
   ```python
   from django.contrib import admin
   from django.urls import path, include

   urlpatterns = [
       path("admin/", admin.site.urls),
       path("api/", include("users.urls")),  # existing DRF routes
   ]
   ```

3. **Migrate & create a superuser**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

4. **Register models (lending/admin.py)**
   ```python
   from django.contrib import admin
   from .models import Merchant, LoanApplication, Offer, Disbursement, Repayment

   @admin.register(Merchant)
   class MerchantAdmin(admin.ModelAdmin):
       list_display = ("id", "name", "status", "created_at")
       search_fields = ("name", "ein", "email_domain")
       list_filter = ("status", "created_at")

   class OfferInline(admin.TabularInline):
       model = Offer
       extra = 0
       readonly_fields = ("amount", "apr", "term_months", "created_at")

   class RepaymentInline(admin.TabularInline):
       model = Repayment
       extra = 0
       readonly_fields = ("amount", "scheduled_for", "received_at", "status")

   @admin.register(LoanApplication)
   class LoanApplicationAdmin(admin.ModelAdmin):
       list_display = ("id","merchant","status","requested_amount","decision","created_at")
       list_filter = ("status","decision","created_at")
       search_fields = ("id","merchant__name","applicant_email")
       inlines = [OfferInline, RepaymentInline]
       readonly_fields = ("id","created_at","updated_at")
   ```

5. **Visit the console**
   - Go to **`/admin/`**, log in with your superuser, and manage data.

## Security & Ops Hardening (Recommended)
- **HTTPS + secure cookies:**
  ```python
  SECURE_SSL_REDIRECT = True
  SESSION_COOKIE_SECURE = True
  CSRF_COOKIE_SECURE = True
  ```
- **Network controls:** Put admin behind VPN or IP allowlist; consider a non-obvious path (e.g., `/internal/cabinet/`).
- **2FA & lockout:** `django-otp` (two-factor), `django-axes` (lockout on brute force).
- **Static assets:** Run `python manage.py collectstatic` in production.
- **Observability:** Use request/DB logs; export metrics to **Prometheus** and visualize in **Grafana**.

## How It Coexists with DRF (Your APIs)
- **DRF** serves programmatic JSON endpoints (JWT-protected).
- **Django Admin** serves a human UI (session login).
- Both read the same **Django models**, so your domain stays consistent across console and APIs.

## Next Steps
1. Register the top 3–5 critical models you manage most (Merchant, LoanApplication, Repayment).
2. Add list filters/search to match common Ops queries (status, merchant, date).
3. Add one or two safe **bulk actions** (e.g., approve/close) to save time.
4. Roll out to a small internal group with least-privilege permissions and iterate.
