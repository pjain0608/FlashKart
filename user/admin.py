from django.contrib import admin
from user.models import BuyerProfile
# Register your models here.

class BuyerProfileAdmin(admin.ModelAdmin):
    # Display the 'user' field in the list view
    list_display = ('user', 'name', 'mobile_number', 'address', 'card_number', 'card_expiry')

    # Optionally, you can add filters and search fields
    search_fields = ('user__username', 'name')
    list_filter = ('user',)

admin.site.register(BuyerProfile, BuyerProfileAdmin)