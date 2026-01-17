from django.shortcuts import render, redirect, get_object_or_404
import random
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import EmailMultiAlternatives
import razorpay
from .models import User, Product, Order, OrderItem
from django.views.decorators.csrf import csrf_exempt


# Public Pages
def home(request):
    return render(request, 'main/index.html')


def about(request):
    return render(request, 'main/about.html')


def contact(request):
    return render(request, 'main/contact.html')


def profile(request):
    if 'user_id' not in request.session:
        return redirect('login')
    user = get_object_or_404(User, id=request.session['user_id'])
    return render(request, 'main/profile.html', {'user': user})

def orders_page(request):
    if 'user_id' not in request.session:
        return redirect('login')
    orders = Order.objects.filter(user_id=request.session['user_id']).order_by('-created_at')
    return render(request, 'main/orders.html', {'orders': orders})

def admin_dashboard(request):
    # Basic protection - should ideally be staff only
    if 'user_id' not in request.session:
        return redirect('login')
    
    orders = Order.objects.all().order_by('-created_at')
    total_revenue = sum(o.total_amount for o in orders)
    total_users = User.objects.count()
    total_products = Product.objects.count()
    
    context = {
        'orders': orders,
        'total_revenue': total_revenue,
        'total_users': total_users,
        'total_products': total_products,
    }
    return render(request, 'main/admin_dashboard.html', context)


# OTP Email
def send_otp_email(email, otp):
    subject = "ClothAura - Email Verification OTP"
    from_email = settings.EMAIL_HOST_USER
    to = [email]

    html_content = f"""
    <html>
        <body>
            <div style="max-width:600px;margin:auto;padding:30px;background:#fff;border-radius:8px;text-align:center;">
                <h1>ClothAura OTP Verification</h1>
                <p>Hello,</p>
                <p>Your OTP for email verification is:</p>
                <div style="font-size:24px;font-weight:bold;padding:15px 25px;background:#facc15;color:#fff;border-radius:6px;letter-spacing:4px;">
                    {otp}
                </div>
                <p>This OTP is valid for a few minutes only. Do not share it with anyone.</p>
            </div>
        </body>
    </html>
    """

    email_msg = EmailMultiAlternatives(subject, "", from_email, to)
    email_msg.attach_alternative(html_content, "text/html")
    email_msg.send()


# User Registration with OTP
def register(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect("register")

        otp = random.randint(100000, 999999)

        request.session['reg_name'] = name
        request.session['reg_email'] = email
        request.session['reg_password'] = password
        request.session['otp'] = otp

        send_otp_email(email, otp)
        messages.success(request, "OTP sent to your email!")
        return redirect("verify_otp")

    return render(request, 'main/register.html')


# OTP Verification
def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get('otp')
        session_otp = str(request.session.get('otp'))

        if entered_otp == session_otp:
            user = User(
                name=request.session['reg_name'],
                email=request.session['reg_email'],
                password=make_password(request.session['reg_password'])
            )
            user.save()

            request.session['user_id'] = user.id
            request.session['user_name'] = user.name

            for key in ['reg_name', 'reg_email', 'reg_password', 'otp']:
                request.session.pop(key, None)

            messages.success(request, f"Registration Successful! Welcome {user.name}.")
            return redirect("home")
        else:
            messages.error(request, "Invalid OTP! Please try again.")

    return render(request, 'main/verify_otp.html')


# User Login
def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "User not found! Please register first.")
            return redirect("login")

        if check_password(password, user.password):
            request.session['user_id'] = user.id
            request.session['user_name'] = user.name
            messages.success(request, f"Welcome {user.name}!")
            return redirect("home")
        else:
            messages.error(request, "Incorrect password!")
            return redirect("login")

    return render(request, 'main/login.html')


# User Logout
def logout(request):
    request.session.flush()
    messages.success(request, "Logged out successfully!")
    return redirect("home")


# Products Pages
def get_allProducts(request):
    products = Product.objects.all().order_by('-id')
    return render(request, 'main/products.html', {'products': products})


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    related_products = Product.objects.filter(category=product.category).exclude(id=id)[:4]
    return render(request, 'main/product_detail.html', {
        'product': product,
        'related_products': related_products
    })


# Add to Cart
def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)

    try:
        qty = int(request.GET.get('qty', 1))
        if qty < 1:
            qty = 1
    except ValueError:
        qty = 1

    cart = request.session.get('cart', {})

    if str(id) in cart:
        if "qty" not in cart[str(id)]:
            cart[str(id)]["qty"] = 0
        cart[str(id)]["qty"] += qty
    else:
        cart[str(id)] = {
            "name": product.name,
            "price": float(product.final_price),  
            "image": product.main_image,
            "qty": qty
        }

    request.session['cart'] = cart
    request.session.modified = True

    messages.success(request, f"{product.name} added to cart ({qty})")
    return redirect('cart_page')


def increase_qty(request, id):
    cart = request.session.get('cart', {})
    if id in cart:
        cart[id]['qty'] += 1
        cart[id]['total_price'] = cart[id]['price'] * cart[id]['qty']
    request.session['cart'] = cart
    return redirect('cart_page')


def decrease_qty(request, id):
    cart = request.session.get('cart', {})
    if id in cart and cart[id]['qty'] > 1:
        cart[id]['qty'] -= 1
        cart[id]['total_price'] = cart[id]['price'] * cart[id]['qty']
    request.session['cart'] = cart
    return redirect('cart_page')

# View Cart Page
def cart_page(request):
    cart = request.session.get('cart', {})

    for item in cart.values():
        item['total_price'] = item['price'] * item['qty']

    total = sum(item['total_price'] for item in cart.values())

    return render(request, 'main/cart.html', {'cart': cart, 'total': total})




# Remove from Cart
def remove_from_cart(request, id):
    cart = request.session.get('cart', {})

    if str(id) in cart:
        del cart[str(id)]
        request.session['cart'] = cart
        request.session.modified = True
        messages.success(request, "Item removed!")

    return redirect('cart_page')




def checkout(request):
    cart = request.session.get('cart', {})

    if not cart:
        messages.warning(request, "Your cart is empty!")
        return redirect('cart_page')

    # Calculate total for each item and grand total
    for item in cart.values():
        item['total_price'] = item['price'] * item['qty']

    total_amount = int(sum(item['total_price'] for item in cart.values()) * 100)  # in paise

    # Create Razorpay order
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    razorpay_order = client.order.create({
        "amount": total_amount,
        "currency": "INR",
        "payment_capture": "1"
    })

    # Fetch user details from session
    user_name = request.session.get('user_name', '')
    user_email = User.objects.get(id=request.session.get('user_id')).email if request.session.get('user_id') else ''

    context = {
        'cart': cart,
        'total': total_amount / 100,  # in INR
        'razorpay_order_id': razorpay_order['id'],
        'razorpay_merchant_key': settings.RAZORPAY_KEY_ID,
        'user_name': user_name,
        'user_email': user_email,
    }

    return render(request, 'main/checkout.html', context)


# -----------------------------
# Payment Success Page
# -----------------------------
def payment_success(request):
    payment_id = request.GET.get('payment_id')
    order_id = request.GET.get('order_id')
    signature = request.GET.get('signature')

    if not (payment_id and order_id and signature):
        messages.error(request, "Payment failed or missing details.")
        return redirect('checkout')

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    params_dict = {
        'razorpay_order_id': order_id,
        'razorpay_payment_id': payment_id,
        'razorpay_signature': signature
    }

    try:
        # Verify Razorpay payment
        client.utility.verify_payment_signature(params_dict)

        # Create Order in DB
        user_id = request.session.get('user_id')
        if not user_id:
             messages.error(request, "User session lost. Please login again.")
             return redirect('login')
        
        user = User.objects.get(id=user_id)
        cart = request.session.get('cart', {})
        total_amount = sum(item['price'] * item['qty'] for item in cart.values())
        address = request.GET.get('address', 'Not Provided')

        order = Order.objects.create(
            user=user,
            total_amount=total_amount,
            payment_id=payment_id,
            razorpay_order_id=order_id,
            status='Paid',
            address=address
        )

        for item_id, item in cart.items():
            product = Product.objects.get(id=item_id)
            OrderItem.objects.create(
                order=order,
                product=product,
                qty=item['qty'],
                price=item['price']
            )

        # Payment successful → clear cart
        request.session['cart'] = {}
        messages.success(request, "Order placed successfully!")

        return render(request, 'main/payment_success.html', {
            'payment_id': payment_id,
            'order_id': order_id
        })
    except razorpay.errors.SignatureVerificationError:
        messages.error(request, "Payment verification failed! Please try again.")
        return redirect('checkout')
    except Exception as e:
        messages.error(request, f"An error occurred: {e}")
        return redirect('checkout')
