# FlashKart E-Commerce Application

FlashKart is an e-commerce platform built using Django. It provides features like user registration, authentication, product browsing, cart management, checkout, and order tracking. It allows users to register, login, add products to their cart, and make purchases either via card payment or cash on delivery (COD).

# Features

-  **User Authentication**: Custom login and registration views using Django’s built-in User model.
-  **Product Management**: Users can browse products, filter by categories, and search by product name.
-  **Cart Management**: Users can add products to their cart, remove items, and view the total price.
-  **Checkout & Payment**: Users can checkout using two payment methods: Credit/Debit Card or Cash on Delivery (COD).
-  **Order Tracking**: Users can view their order history and track the status of orders.

# Technologies Used
-  **Django**: The backend framework used for building the application.
-  **MySQ**L: Database management system used for storing product, order, and user data.
-  **HTML/CSS/JavaScript**: Frontend technologies for building user interfaces.
-  **ReCAPTCHA**: Used to prevent bot registrations during user sign-up.
-  **Email Service**: Sends email confirmations to users upon successful registration and order placement.

# How It Works

-  User Registration
      1.Users can create an account by filling out a registration form that includes their name, email, and password.
      2.Passwords are securely hashed using Django’s built-in functionality.
      3.A profile is created for the user with additional information such as name, mobile number, address, and card details.
-  Login & Logout
      1.Users can log in using their registered username and password.
      2.After login, they are redirected to the product list or cart page, depending on the route they are coming from.
      3.Users can log out, and the session is cleared.
-  Product Browsing & Cart
      1.Users can browse products, filter by category, or search for products.
      2.Users can add products to their cart with a specified quantity.
      3.Users can view their cart, remove items, and see the total price.
-  Checkout & Payment
      1.Users can proceed to checkout and choose between Card or Cash on Delivery (COD) for payment.
      2.For Card payments, users must enter the last four digits and CVV of their card for validation.
      3.Upon successful checkout, the order is created, and an email confirmation is sent to the user.
-  Order History
      1.Users can view their past orders, track their current order status, and receive email notifications for order updates.

# File Structure

flashkart/  <br>
│  <br>
├── flashkart/           # Main Django project directory  <br>
│   ├── __init__.py  <br>
│   ├── settings.py  <br>
│   ├── urls.py  <br>
│   └── wsgi.py  <br>
│  <br>
├── products/            # Django app for handling products, cart, and orders <br>
│   ├── __init__.py <br>
│   ├── models.py        # Defines the models for Product, Order, Cart, etc. <br>
│   ├── views.py         # Contains views for handling user actions <br>
│   ├── forms.py         # Defines the forms for user registration and profile <br>
│   └── templates/ <br>
│       ├── register.html <br>
│       ├── login.html <br>
│       ├── product_list.html <br>
│       └── checkout.html <br>
│ <br>
└── manage.py            # Django management script <br>

# UI View
![Image](https://github.com/user-attachments/assets/f558bf55-51d3-416d-9780-1fb3608d6c95)  <br>

![Image](https://github.com/user-attachments/assets/a1a6dd82-5783-4f99-9886-49dfcbe1134c)  <br>

![Image](https://github.com/user-attachments/assets/24954804-ce08-4c6e-9f28-6404a1db39ac) <br>

![Image](https://github.com/user-attachments/assets/238ab461-5531-4e47-8839-fbbe80bdf020) <br>

![Image](https://github.com/user-attachments/assets/e71d23c5-28fc-4c64-ade4-a9ed7690e056) <br>

![Image](https://github.com/user-attachments/assets/4762b4d3-5cac-44da-8df7-1c58daba382c) <br>

![Image](https://github.com/user-attachments/assets/5da0dca1-d6d7-4d2d-9739-033ab2f0b580) <br>

![Image](https://github.com/user-attachments/assets/984cb15a-22a4-4dd8-9472-59f425a0445a) <br>

![Image](https://github.com/user-attachments/assets/1a6fa12f-a852-42d0-9d63-23df873d1eb8) <br>
