from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, CartItem, Order, Payment, Category, PaymentStatus, PayMode
from user.models import BuyerProfile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import random

def login_view(request):
    """
    Custom login view.
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Authenticate and log the user in
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('product_list')  # Redirect to product list or any other page
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    """
    Custom logout view.
    """
    logout(request)
    return redirect('product_list')

def product_list(request):
    categories = Category.objects.all()
    selected_category = request.GET.get('category')
    search_query = request.GET.get('search')  # Get the search query from the GET parameters
    
    # Filter products based on category if selected
    if selected_category:
        products = Product.objects.filter(category__id=selected_category)
    else:
        products = Product.objects.all()
    
    # If search query is provided, filter products by name
    if search_query:
        products = products.filter(name__icontains=search_query)  # Use icontains for case-insensitive search
    
    user = request.user
    user_profile = user.buyerprofile if user.is_authenticated else None  # Use buyerprofile instead of profile
    

    return render(request, "product_list.html", {'products': products, 'categories': categories, 'user_profile': user_profile})

@login_required(login_url='login')
def cart_view(request):
    cart = Cart.objects.filter(buyer=request.user).first()  # Assuming a user is logged in and has a cart
    if cart:
        cart_items = CartItem.objects.filter(cart=cart)
        total_price = sum(item.product.price * item.quantity for item in cart_items)
    else:
        cart_items = []
        total_price = 0
    
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required(login_url='login')
def add_to_cart(request, product_id):
    """
    View to add a product to the cart with support for custom quantities.
    """
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(buyer=request.user)

    # Fetch quantity from the form (default to 1 if not provided)
    quantity = int(request.POST.get('quantity', 1))  # Default to 1 if no quantity is submitted

    # Check if the CartItem already exists for the given product
    cart_item = CartItem.objects.filter(cart=cart, product=product).first()

    if not cart_item:
        # If CartItem does not exist, create it with the provided quantity
        cart_item = CartItem.objects.create(cart=cart, product=product, quantity=quantity)
    else:
        # If CartItem exists, update the quantity
        cart_item.quantity += quantity
        cart_item.save()

    return redirect('home')

@login_required(login_url='login')
def remove_from_cart(request, item_id):
    """
    View to remove an item from the cart.
    """
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect('cart_view')

@login_required(login_url='login')
def checkout(request):
    """
    View to handle the checkout process with card validation.
    """
    cart = get_object_or_404(Cart, buyer=request.user)

    if request.method == "POST":
        payment_method = request.POST.get('payment_method')

        try:
            # Retrieve the buyer profile (common for both payment methods)
            buyer_profile = BuyerProfile.objects.get(user=request.user)
        except BuyerProfile.DoesNotExist:
            messages.error(request, "No buyer profile found for this account.")
            return redirect('checkout')

        if payment_method == 'Card':
            last_four_digits = request.POST.get('last_four_digits')
            cvv = request.POST.get('cvv')

            # Validate card details against the database
            full_card_number = buyer_profile.card_number
            if not full_card_number.endswith(last_four_digits):
                messages.error(request, "Invalid card details. The last four digits do not match.")
                return redirect('checkout')

            if buyer_profile.card_cvv != cvv:
                messages.error(request, "Invalid CVV. Please try again.")
                return redirect('checkout')

            # Payment status and mode for Card
            payment_status = PaymentStatus.objects.get(pay_status="Paid")  # Assuming "Paid" is the status
            payment_mode = PayMode.objects.get(pay_mode="Card")  # Assuming "Card" is the mode

        elif payment_method == 'COD':
            # Payment status and mode for COD
            payment_status = PaymentStatus.objects.get(pay_status="UnPaid")  # Assuming "Not Paid" for COD
            payment_mode = PayMode.objects.get(pay_mode="COD")  # Assuming "COD" is the mode

        # Create the order
        order = Order.objects.create(buyer=request.user, total_price=cart.total_price())
        order.product.set(cart.products.all())

        # Create the payment entry
        Payment.objects.create(
            order=order,
            mode_of_payment=payment_mode,
            payment_status=payment_status,
            last_four_digits=last_four_digits if payment_method == "Card" else None,
            cvv=cvv if payment_method == "Card" else None,
        )

        # Clear cart after order
        cart.cartitem_set.all().delete()

        # Prepare email content
        subject = f"Order Confirmation - {order.order_id}"
        message = f"""
        Dear {buyer_profile.name},

        Thank you for your purchase! Your order has been successfully placed. Below are the details:

        Order ID: {order.order_id}
        Status: {payment_status.pay_status}

        Best Regards,
        The FlashKart Team
        """

        # Send the email
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [request.user.email],
            fail_silently=False,
        )

        # Redirect to the order confirmation page
        messages.success(request, "Your order has been placed successfully.")
        return redirect('order_confirmation', order_id=order.id)

    return render(request, "checkout.html", {"cart": cart})

@login_required(login_url='login')
def order_confirmation(request, order_id):
    """
    View to display the order confirmation after placing an order.
    """
    order = get_object_or_404(Order, id=order_id)
    return render(request, "order_confirmation.html", {"order": order})

@login_required(login_url='login')
def order_history(request):
    """
    View to display past orders for the logged-in user.
    """
    orders = Order.objects.filter(buyer=request.user)
    return render(request, "order_history.html", {"orders": orders})

@login_required(login_url='login')
def remove_from_cart(request, item_id):
    """
    View to remove an item from the cart.
    """
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect('cart_view')  # Redirect to the cart page after removing the item

