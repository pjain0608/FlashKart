from django.db import models
from django.contrib.auth.models import User
import random

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('Being Packed', 'Being Packed'),
        ('In Transit', 'In Transit'),
        ('Delivered', 'Delivered'),
    ]
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Being Packed')
    created_at = models.DateTimeField(auto_now_add=True)
    order_id = models.CharField(max_length=25, unique=True, blank=True)         #For creating Order ID

    def save(self, *args, **kwargs):
    # Generate a unique order ID if not already set
        if not self.order_id:
            # Find the last order created
            last_order = Order.objects.all().order_by('created_at').last()

            if last_order:
                # Directly get the last order number and increment it
                last_order_number = int(last_order.order_id)
                new_order_number = last_order_number + 1
            else:
                # Start the first order number from 123000000000001
                new_order_number = 123000000000001

            # Set the new order_id
            self.order_id = f"{new_order_number}"

        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"Order {self.id} by {self.buyer.username}"

class Cart(models.Model):
    buyer = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem')

    def total_price(self):
        return sum(item.product.price * item.quantity for item in self.cartitem_set.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class PaymentStatus(models.Model):
    pay_status = models.CharField(max_length=20)

    def __str__(self):
        return self.pay_status

class PayMode(models.Model):
    pay_mode = models.CharField(max_length=20)

    def __str__(self):
        return self.pay_mode

class Payment(models.Model):

    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    mode_of_payment = models.ForeignKey(PayMode, on_delete=models.CASCADE)
    payment_status = models.ForeignKey(PaymentStatus, on_delete=models.CASCADE)

    # Card details for validation (only stored temporarily)
    last_four_digits = models.CharField(max_length=4, blank=True, null=True)
    cvv = models.CharField(max_length=3, blank=True, null=True)

    def __str__(self):
        return f"Payment for Order {self.order.order_id}"
