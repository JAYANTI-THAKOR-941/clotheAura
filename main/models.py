from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# =========================
# User Model
# =========================
class User(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=225)
    mobile = models.CharField(max_length=15, null=True, blank=True)
    profile_image = models.URLField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Password handling
    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.email


# =========================
# Product Model
# =========================
class Product(models.Model):
    # Basic Info
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100, null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)  # e.g., Shirt, T-Shirt
    color = models.CharField(max_length=50, null=True, blank=True)
    material = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=20, null=True, blank=True)  # e.g., Male, Female, Unisex

    # Description
    short_description = models.CharField(max_length=300, null=True, blank=True)
    long_description = models.TextField(null=True, blank=True)
    features = models.TextField(null=True, blank=True)  # multiline features

    # Sizes
    SIZES = [
        ('XS','Extra Small'),
        ('S','Small'),
        ('M','Medium'),
        ('L','Large'),
        ('XL','Extra Large'),
        ('XXL','2XL'),
        ('3XL','3XL'),
    ]
    size = models.CharField(max_length=5, choices=SIZES, null=True, blank=True)

    # Pricing & Stock
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.PositiveIntegerField(default=0)  # discount in percentage
    in_stock = models.BooleanField(default=True)
    stock = models.PositiveIntegerField(default=1)

    # Images
    main_image = models.URLField(max_length=500, null=True, blank=True)
    gallery_images = models.JSONField(null=True, blank=True)

    # Meta
    created_at = models.DateTimeField(auto_now_add=True)

    # Calculated property for discounted price
    @property
    def final_price(self):
        if self.discount > 0:
            return self.price - (self.price * self.discount / 100)
        return self.price

    def __str__(self):
        return self.name


# =========================
# Order Model
# =========================
class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_order_id = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.email}"


# =========================
# OrderItem Model
# =========================
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.qty} x {self.product.name}"
