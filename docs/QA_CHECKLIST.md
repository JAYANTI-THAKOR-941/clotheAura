# Manual acceptance testing

Use an isolated database, fictional customers and payment-provider test mode. Record actual observations and never record real secrets.

| ID | Test | Expected outcome |
|---|---|---|
| QA01 | Open catalogue | Product list renders without errors |
| QA02 | Unknown product ID | Safe not-found response |
| QA03 | Register with duplicate email | Account creation rejected |
| QA04 | Invalid OTP | No authenticated session |
| QA05 | Correct test OTP | Account created only once |
| QA06 | Invalid password | Login rejected |
| QA07 | Logged-out profile access | Redirect to login |
| QA08 | Add and remove cart product | Quantity and total match |
| QA09 | Quantity beyond stock | Reject or safely limit quantity |
| QA10 | Discount of 10% on 100.00 | Decimal price 90.00 |
| QA11 | Tampered checkout amount | Server recomputes price |
| QA12 | Invalid payment signature | No paid order |
| QA13 | Repeated payment callback | No duplicate order |
| QA14 | Non-admin visits dashboard | Access denied |
| QA15 | Different user requests an order | No access to another user's order |
| QA16 | Mobile viewport | Catalogue and cart remain usable |

These are acceptance targets, not recorded test results. Failures should become issues and be fixed before deployment.
