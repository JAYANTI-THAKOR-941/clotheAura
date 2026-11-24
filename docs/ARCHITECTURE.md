# Architecture and developer guide

## Current implementation
ClothAura is a Django 6 project with the `main` application and server-rendered templates. The source currently defines User, Product, Order and OrderItem models. The User model uses Django password hashers but is separate from Django's built-in authentication user. The storefront uses session-based authentication and cart state.

| Model | Responsibility |
|---|---|
| User | Unique email, hashed password, name and optional profile information |
| Product | Catalogue, sizes, images, Decimal price, percentage discount, stock |
| Order | User relationship, amount, address, payment references and status |
| OrderItem | Order and product relationships, quantity and recorded unit price |

## Request flow
Browser → Django URL resolver → view → model or session → template response.

Registration stores pending registration details in the session and verifies an OTP before creating the user. Login stores a user identifier in the session. Cart operations change session state. Checkout uses Razorpay; order records include payment references. These descriptions describe the existing source, not a security guarantee.

## Local development
Use Python 3.12 or later for Django 6. Create a virtual environment and install requirements.txt. Inspect settings before starting; use only local test database and sandbox credentials.

```sh
python -m venv .venv
# Activate .venv for your operating system.
python -m pip install -r requirements.txt
python manage.py check
python manage.py migrate
python manage.py runserver
```

Use Django's built-in admin only with proper administrator credentials. Never deploy a development server to production. See [security review checklist](SECURITY_REVIEW.md) and [manual acceptance tests](QA_CHECKLIST.md).

## Routes
| Path | Purpose |
|---|---|
| / | Home |
| /register/, /verify_otp/, /login/ | Account flow |
| /products/, /products/<id>/ | Catalogue |
| /cart/ | Session cart |
| /checkout/, /payment-success/ | Payment flow |
| /orders/, /profile/ | Account pages |
| /admin-dashboard/ | Custom dashboard; authorization requires verification |

## Proposed improvements
Use a standard authentication model, formal role checks, atomic stock and order operations, explicit payment state transitions, and a service layer for checkout. These are roadmap items, not implemented features.
