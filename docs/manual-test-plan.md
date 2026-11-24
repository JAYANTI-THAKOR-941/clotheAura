# Manual acceptance tests

Use an isolated local database, fictional accounts and sandbox services. Record actual results separately; all cases below are proposed, not passed test results.

| ID | Scenario | Expected result |
|---|---|---|
| T01 | Browse product catalogue | Product list and detail render |
| T02 | Register a fictional user | Validation and verification flow start |
| T03 | Submit invalid or expired OTP | Verification refused |
| T04 | Log in with valid test credentials | Authorized session created |
| T05 | Add a product to cart | Item and quantity appear |
| T06 | Increase and decrease quantity | Totals update; invalid quantities rejected |
| T07 | Remove cart item | Item removed and totals recomputed |
| T08 | Try checkout with empty cart | Checkout rejected or redirected |
| T09 | Inspect order as unrelated user | Access denied |
| T10 | Visit admin route as ordinary user | Access denied |
| T11 | Submit sandbox payment success | Verify provider signature and amount before fulfillment |
| T12 | Repeat payment callback | No duplicate order or charge fulfillment |
| T13 | Submit state-changing request without CSRF token | Request denied where CSRF protection applies |
| T14 | Try unavailable stock | Server rejects oversell |
| T15 | Log out | Protected pages require authentication |

## Regression checklist
Run Django system checks, migration checks and automated tests before deployment. Review security settings and dependencies. Capture screenshots only with fictional data.
