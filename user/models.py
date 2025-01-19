from django.db import models
from django.contrib.auth.models import User

class BuyerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    address = models.TextField()
    card_number = models.CharField(max_length=16)
    card_expiry = models.CharField(max_length=5)  # MM/YY format
    card_cvv = models.CharField(max_length=3)
    
    def __str__(self):
        return self.user.username
