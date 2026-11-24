# ClothAura architecture and development guide

## Existing application
The Django project contains the ClothAura configuration package and main application. The main app has User, Product, Order and OrderItem models, storefront views, account registration and OTP verification, cart operations, checkout and a payment-success view. These are existing components, not a guarantee that every flow is production-ready.

## Development workflow
1. Create an isolated virtual environment: python -m venv .venv.
2. Activate it and install requirements.txt.
3. Review settings privately. Configure development database, email and payment settings without committing credentials.
4. Run python manage.py check and python manage.py migrate.
5. Run python manage.py runserver on localhost.
6. Use fictional accounts and payment sandbox credentials only.

## Request flow
Browser → Django URL routing → view → model/database or session → template response.
Registration and verification establish identity; authorization must be checked separately on every protected view. Cart quantities and product prices must be validated on the server. Payment success requires independent server-side verification with the provider before order fulfillment.

## Suggested production improvements
- Require POST and CSRF protection for mutations.
- Validate quantities and stock atomically.
- Use Decimal for money and compute totals on the server.
- Apply ownership and role checks to orders and admin operations.
- Limit OTP retries, expire codes and avoid storing them in logs.
- Verify payment signatures, order identity and amount; handle repeated callbacks idempotently.
- Load secrets from environment variables, disable debug and configure allowed hosts and HTTPS.

## Troubleshooting
If migrations fail, inspect the migration status and database configuration before modifying data. If templates fail, check URL names, template locations and context keys. For email errors, check sandbox SMTP configuration and provider requirements. For payment errors, confirm sandbox configuration and compare provider transaction status.
