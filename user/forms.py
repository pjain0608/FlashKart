from django import forms
from django.contrib.auth.models import User
from .models import BuyerProfile
from django_recaptcha.fields import ReCaptchaField


class RegisterForm(forms.ModelForm):
    
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    

    class Meta:
        model = User
        fields = ['username', 'email']  # username and email are the fields for the User model

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match!")

        # Add password to cleaned_data for saving
        cleaned_data['password'] = password
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Hash the password before saving
        if commit:
            user.save()
        return user

class BuyerProfileForm(forms.ModelForm):
    recaptcha = ReCaptchaField()
    class Meta:
        model = BuyerProfile
        fields = ['name', 'mobile_number', 'address', 'card_number', 'card_expiry', 'card_cvv']
