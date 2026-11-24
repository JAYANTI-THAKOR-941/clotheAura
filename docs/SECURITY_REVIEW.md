# Security and deployment review

The following are release requirements to verify, not claims that the application already satisfies them.

- Keep secret keys, email credentials and payment keys in ignored environment configuration. Rotate any exposed credentials and inspect history.
- Enforce server-side administrator authorization; a session user ID alone does not establish an administrator role.
- Use POST and CSRF protection for state-changing actions, including cart updates and logout.
- Apply OTP expiration, attempt limits and resend throttling; do not retain plaintext passwords in sessions. Prefer Django authentication and rotate session identifiers on login.
- Recompute order totals and stock on the server. Verify payment signatures, amount, currency and ownership using the payment provider. Make completion idempotent and transactional.
- Validate discounts within 0–100%, prices and available quantities; use Decimal and explicit currency rounding.
- Enforce HTTPS, secure cookies, allowed hosts, safe production settings and protected logs.
- Review dependency advisories, database backups, access controls and recovery procedures.

Run `python manage.py check --deploy` against intended production settings. Passing this command is not a complete security audit. Do not use real money in an unverified checkout.
