from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import RegisterForm, BuyerProfileForm
from .models import BuyerProfile
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
from django.core.mail import send_mail

def register(request):
    if request.method == "POST":
        user_form = RegisterForm(request.POST)
        profile_form = BuyerProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            # Save user and buyer profile
            user = user_form.save()  # Save the user
            profile = profile_form.save(commit=False)  # Do not save profile yet
            profile.user = user  # Link the profile to the user
            profile.save()

            # Fetch the name, mobile, email, and address from the BuyerProfile model
            name = profile.name
            mobile_number = profile.mobile_number
            email = user.email  # Email is part of the user model
            address = profile.address

            # Compose the email message manually
            subject = "Welcome to FlashKart!"
            message = f"""
            Hello {name},

            Thank you for registering with FlashKart! Here are your registration details:

            Name: {name}
            Mobile: {mobile_number}
            Email: {email}
            Address: {address}

            If you have any questions or need assistance, feel free to contact us.

            Best regards,
            The FlashKart Team
            """

            # Send the email to the user
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,  # Default from email set in settings
                [email],
                fail_silently=False
            )

            return redirect('register_success')  # Redirect to success page or wherever you want
        else:
            return render(request, "register.html", {"user_form": user_form, "profile_form": profile_form})

    else:
        user_form = RegisterForm()
        profile_form = BuyerProfileForm()

    return render(request, "register.html", {"user_form": user_form, "profile_form": profile_form})

def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
            # Get the username and password from the cleaned data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Authenticate the user
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                # Redirect to the next page (cart or home)
                next_url = request.GET.get('next', '/')
                return redirect(next_url)
            else:
                return render(request, "login.html", {"error": "Invalid credentials", "form": form})
        else:
            return render(request, "login.html", {"error": "Both fields are required", "form": form})
    else:
        form = AuthenticationForm()
        return render(request, "login.html", {"form": form})

def logout_user(request):
    logout(request)
    return redirect('/')

def register_success(request):
    return render(request, 'register_success.html')

def user_profile(request):
    # Get the currently logged-in user
    user = request.user
    
    # Fetch the corresponding BuyerProfile
    profile = get_object_or_404(BuyerProfile, user=user)
    
    return render(request, 'user_profile.html', {'profile': profile})