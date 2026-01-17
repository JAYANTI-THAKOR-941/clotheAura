from django.urls import path
from . import views

urlpatterns = [
    # ✅ Public Pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('profile/', views.profile, name='profile'),

    # ✅ Authentication
    path('register/', views.register, name='register'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    # ✅ Products
    path('products/', views.get_allProducts, name='products'),
    path('products/<int:id>/', views.product_detail, name='product_detail'),

    # 🛒 Cart Routes
    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),  # Add item to cart
    path('cart/', views.cart_page, name='cart_page'),                        # View cart
    path('cart/remove/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/increase/<str:id>/', views.increase_qty, name='increase_qty'),
    path('cart/decrease/<str:id>/', views.decrease_qty, name='decrease_qty'),
  # Remove item

    path('checkout/', views.checkout, name='checkout'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('orders/', views.orders_page, name='orders'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
