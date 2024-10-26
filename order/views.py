from django.shortcuts import render,redirect, HttpResponse
from django.contrib import messages 
from .models import UserCopy
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import *

from django.http import JsonResponse
from .models import Dish

from .models import DeliverySettings
from .forms import LocationForm

from django.contrib.auth import logout
import google.generativeai as genai
from dotenv import load_dotenv

import os


def logout_user(request):
    print("here logout")
    logout(request)
    return redirect("/")






# Create your views here.

def offers_view(request):
    offers = Offer.objects.all()
    return render(request, 'offers.html', {'offers': offers})


def index(request):
    top_products = Dish.objects.all()[:5]  # Fetch top products from the database
    gallery_items = Gallery.objects.all()  # Fetch all gallery items

    # Combine both querysets into the context dictionary
    context = {
        'top_products': top_products,
        'gallery_items': gallery_items
    }

    # Pass both top_products and gallery_items to the template
    return render(request, 'index.html', context)



def signup(request):

    if request.method == 'POST':
        username = request.POST.get('Username')
        Email = request.POST.get('Email')
        PhoneNumber = request.POST.get('PhoneNumber')
        Password = request.POST.get('Password')
        CPassword = request.POST.get('ConfirmPassword')
        u=userinfo()
        u.username=username
        u.email=Email
        u.save()
        
    
        if Password==CPassword:
            if UserCopy.objects.filter(phone_number=PhoneNumber).exists():
                messages.info(request, 'Phone Number already registered')
                return redirect('signup')
            
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username already Taken')
                return redirect('signup')
            
            else :
                user = User()
                user.username=Email
                user.password=Password
                user.set_password=Password
                user.save()
        
                user_copy = UserCopy(user=user, password=Password, email=Email, phone_number = PhoneNumber, username = username)
                user_copy.save()

                return redirect('login')
    
        else:
            messages.info(request, "Password does not match")
            return redirect('signup')
        
    else:
        return render(request, 'signup.html')

def login(request):

    if request.method == 'POST':

        user_email = request.POST['email']
        user_password = request.POST['password']

        user = auth.authenticate(username = user_email, password = user_password)
        print(user)
        # print(UserCopy.objects.get(email = user_email))
        try:
            myuser = UserCopy.objects.get(email = user_email)
            # myuser = UserCopy.objects.get(password = user_password)
            
        except Exception as e:
            myuser = None
            print(e)  
        if myuser is not None:
            user = myuser.user 
            auth.login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Invalid credentials. Please try again.')
            return render(request, 'login.html')
    
    return render(request, 'login.html')




def home(request):

    top_products = Menu.objects.all()  # Fetch all top products from the database
    return render(request, '', {'top_products': top_products})



def gallery_view(request):
    # Fetch all gallery items
    gallery_items = Gallery.objects.all()
    return render(request, 'gallery.html', {'gallery_items': gallery_items})





# View for displaying the meals (menu items)
def meals(request):
    meals = Menu.objects.all()  # Fetch all meal categories
    return render(request, 'meal.html', {'meals': meals})

# View for displaying dishes associated with a specific meal
def dish(request, meal_id):
    meal = get_object_or_404(Menu, id=meal_id)  # Fetch the selected meal
    dishes = Dish.objects.filter(menu=meal)  # Fetch all dishes in that meal
    return render(request, 'dish.html', {'meal': meal, 'dishes': dishes})





@login_required(login_url='/login/')
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cart_items.all()
    return render(request, 'cart.html', {'cart': cart, 'cart_items': cart_items})

def add_to_cart(request, item_type, item_id):
    cart, created = Cart.objects.get_or_create(user=request.user)

    if item_type == 'dish':
        dish = get_object_or_404(Dish, id=item_id)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, dish=dish)
    elif item_type == 'combo':
        combo = get_object_or_404(combo, id=item_id)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, combo=combo)
    elif item_type == 'offer':
        offer = get_object_or_404(offer, id=item_id)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, offer=offer)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    cart.update_total_price()
    return redirect('view_cart')

def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()
    cart_item.cart.update_total_price()
    return redirect('view_cart')

def update_cart_quantity(request, cart_item_id, action):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)

    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease' and cart_item.quantity > 1:
        cart_item.quantity -= 1
    
    cart_item.save()
    cart_item.cart.update_total_price()
    return redirect('view_cart')



def about_dish(request, dish_id):
    # Fetch the specific dish using the ID from the URL
    dish = get_object_or_404(Dish, id=dish_id)
    
    # Handle form submission for adding items to the cart
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))  # Default quantity is 1 if not specified
        cart_item, created = Cart.objects.get_or_create(dish=dish, defaults={'quantity': quantity})
        
        if not created:
            # If the item already exists in the cart, update the quantity
            cart_item.quantity += quantity
            cart_item.save()
        
        return redirect('cart_page')  # Redirect to cart page after adding item
    
    context = {
        'dish': dish,
    }
    
    return render(request, 'about.html', context)




from django.shortcuts import render, get_object_or_404, redirect
from .models import Dish, Cart, CartItem

# About page for Dish
def about_dish(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)

    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Get or create a cart for the logged-in user
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        # Handle anonymous users with a session-based cart
        cart = request.session.get('cart', {})

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))

        if request.user.is_authenticated:
            # Add items to the cart for authenticated users
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                dish=dish,
                defaults={'quantity': quantity, 'price': dish.price * quantity}
            )
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
        else:
            # Add items to the session cart for anonymous users
            cart[str(dish.id)] = {
                'name': dish.name,
                'quantity': quantity,
                'price': str(dish.price * quantity),
            }
            request.session['cart'] = cart

        return redirect('view_cart')

    context = {
        'dish': dish,
    }
    return render(request, 'about.html', context)




def about_combo(request, combo_id):
    combo = get_object_or_404(combo, id=combo_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            combo=combo,
            defaults={'quantity': quantity, 'price': combo.price * quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return redirect('cart_page')

    context = {
        'combo': combo,
    }
    return render(request, 'about.html', context)







@login_required
def place_order(request):
    # Get the user's cart
    cart = get_object_or_404(Cart, user=request.user)

    # Use the related name 'cart_items' to get all cart items
    cart_items = cart.cart_items.all()  

    if not cart_items:
        return redirect('index')  # Redirect if the cart is empty

    # Calculate total price
    total_price = sum(item.get_total_price() for item in cart_items)

    # Get or create the UserCopy instance based on the logged-in user
    user_copy, created = UserCopy.objects.get_or_create(
        username=request.user.username, 
        # defaults={'phone_number': request.user.phone_number}  # Adjust if needed
    )

    # Create an order
    # Assuming user_copy is an instance of UserCopy
    original_user = user_copy.user  # Access the related User instance from UserCopy

    # Now you can create the order with the actual User instance
    order = Order.objects.create(
    user=original_user,  # Assign the User instance
    total_price=total_price,
    status='Pending'  # Default status
   )

   

    # Create OrderItems for each cart item
    for cart_item in cart_items:
        OrderItem.objects.create(
            order=order,
            dish=cart_item.dish,
            # combo=cart_item.combo,
            quantity=cart_item.quantity
        )

    # Clear the cart after placing the order
    cart.cart_items.all().delete()  # Deleting all cart items
    cart.total_price = 0.00  # Resetting the total price
    cart.save()  # Save the updated cart

    return redirect('meals', order_id=order.id)










from django.shortcuts import render
from .forms import LocationForm
from .utils import get_coordinates_opencage, calculate_distance  # Import the OpenCage function
from .models import DeliverySettings

def check_delivery(request):
    message = ""
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            user_location = form.cleaned_data['location']
            user_lat, user_lng = get_coordinates_opencage(user_location)  # Get user coordinates using OpenCage
            
            if user_lat and user_lng:
                # Get the delivery settings from the admin (restaurant's location and delivery radius)
                delivery_settings = DeliverySettings.objects.first()
                
                if delivery_settings:
                    restaurant_lat = delivery_settings.restaurant_lat
                    restaurant_lng = delivery_settings.restaurant_lng
                    delivery_radius = delivery_settings.delivery_radius

                    # Calculate the distance between the user's location and the restaurant
                    distance = calculate_distance(restaurant_lat, restaurant_lng, user_lat, user_lng)

                    if distance <= delivery_radius:
                        message = f"Delivery is available to your location ({distance:.2f} km away)."
                    else:
                        message = f"Sorry, delivery is not available. You are {distance:.2f} km away, which exceeds the delivery radius of {delivery_radius} km."
                else:
                    message = "Delivery settings are not configured yet."
            else:
                message = "Could not find your location. Please try again."
    else:
        form = LocationForm()

    return render(request, 'check_delivery.html', {'form': form, 'message': message})





from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Cart, CartItem, Order, OrderItem, DeliverySettings
from .utils import get_coordinates_opencage, calculate_distance

@login_required
def place_order(request):
    # Get the user's cart
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.cart_items.all()

    if not cart_items:
        messages.error(request, "Your cart is empty. Please add items before placing an order.")
        return redirect('view_cart')

    # Calculate total price
    total_price = sum(item.get_total_price() for item in cart_items)

    if request.method == "POST":
        # Get the order type from the form
        order_type = request.POST.get('order_type')

        # Handle order type 'pickup'
        mail = request.user
        userobj = userinfo.objects.get(email = mail)
        if order_type == 'pickup':
            order = Order.objects.create(
                user=userobj,
                total_price=total_price,
                order_mode='pickup'
            )
            # Create OrderItems for each cart item
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    dish=cart_item.dish,
                    quantity=cart_item.quantity
                )
            # Clear the cart
            cart.cart_items.all().delete()
            cart.total_price = 0.00
            cart.save()

            messages.success(request, "Your pickup order has been placed successfully!")
            return redirect('/')

        # Handle order type 'delivery'
        elif order_type == 'delivery':
            address = request.POST.get('address')
            if not address:
                messages.error(request, "Please enter a delivery address.")
                return redirect('choose_order_type')  # Redirect back if address is missing

            # Get delivery coordinates
            user_lat, user_lng = get_coordinates_opencage(address)

            if user_lat and user_lng:
                # Get delivery settings from admin
                delivery_settings = DeliverySettings.objects.first()

                if delivery_settings:
                    distance = calculate_distance(
                        delivery_settings.restaurant_lat,
                        delivery_settings.restaurant_lng,
                        user_lat,
                        user_lng
                    )
                    mail = request.user
                    # print(mail)
                    userobj=userinfo.objects.get(email=mail)
                    if distance <= delivery_settings.delivery_radius:
                        order = Order.objects.create(

                            user=userobj,
                            total_price=total_price,
                            order_mode='delivery',
                            address=address
                        )
                        # Create OrderItems for each cart item
                        for cart_item in cart_items:
                            OrderItem.objects.create(
                                order=order,
                                dish=cart_item.dish,
                                quantity=cart_item.quantity
                            )
                        # Clear the cart
                        cart.cart_items.all().delete()
                        cart.total_price = 0.00
                        cart.save()

                        messages.success(request, f"Your delivery order has been placed successfully! (Distance: {distance:.2f} km)")
                        return redirect('/')
                    else:
                        messages.error(request, f"Sorry, delivery is not available. Your location is {distance:.2f} km away, exceeding the {delivery_settings.delivery_radius} km limit.")
                        return redirect('choose_order_type')
                else:
                    messages.error(request, "Delivery settings are not configured.")
                    return redirect('choose_order_type')
            else:
                messages.error(request, "Could not find your location. Please try again.")
                return redirect('choose_order_type')

    return redirect('view_cart')






@login_required
def choose_order_type(request):
    # Check if the user has items in the cart
    cart = Cart.objects.filter(user=request.user).first()
    if not cart or not cart.cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('view_cart')

    return render(request, 'choose_order_type.html')  # Render the order selection page





from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import UserCopy, Order

@login_required
def account_page(request):
    # Get the user's copy details
    user_copy = UserCopy.objects.get(user=request.user)

    # Get the user's orders
    orders = Order.objects.filter(user=request.user)

    # Pass the user information and orders to the template
    context = {
        'user_copy': user_copy,
        'orders': orders
    }
    return render(request, 'account.html', context)







