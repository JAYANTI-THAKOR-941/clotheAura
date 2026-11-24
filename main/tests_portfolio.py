from decimal import Decimal
from django.test import SimpleTestCase
from .models import Product, User


class ProductPricingTests(SimpleTestCase):
    def test_discounted_price(self):
        product = Product(name="Sample", price=Decimal("100.00"), discount=10)
        self.assertEqual(product.final_price, Decimal("90.00"))

    def test_no_discount(self):
        product = Product(name="Sample", price=Decimal("125.50"), discount=0)
        self.assertEqual(product.final_price, Decimal("125.50"))


class PasswordHashTests(SimpleTestCase):
    def test_password_is_hashed_and_checked(self):
        user = User(name="Sample", email="sample@example.test")
        user.set_password("fictional-local-test-password")
        self.assertNotEqual(user.password, "fictional-local-test-password")
        self.assertTrue(user.check_password("fictional-local-test-password"))
        self.assertFalse(user.check_password("incorrect"))
