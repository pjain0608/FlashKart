# flashkart/admin.py

from django.contrib import admin
from .models import Product, Cart, CartItem, Order, Payment, Category, PaymentStatus, PayMode

admin.site.register(Category)

# Register the Product model in the admin interface
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description', 'image')
    search_fields = ('name', 'description')
    ordering = ('name',)

# Register the Cart model in the admin interface
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('buyer',)
    search_fields = ('buyer__username',)

# Register the CartItem model in the admin interface
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')
    search_fields = ('cart__buyer__username', 'product__name')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'buyer', 'total_price', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('order_id', 'buyer__username')

admin.site.register(PaymentStatus)
admin.site.register(PayMode)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'mode_of_payment', 'payment_status')
    list_filter = ('payment_status', 'mode_of_payment')