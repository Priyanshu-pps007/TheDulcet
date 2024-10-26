from django.db import models
from django.contrib.auth.models import User  # or use your UserCopy model
from django.utils import timezone
from datetime import timedelta

# UserCopy model for reference
class UserCopy(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    password = models.CharField(max_length=25, null=True, blank=True)
    phone_number = models.IntegerField(unique=True, null=True, blank=True)
    username = models.CharField(max_length=25, unique=True)
    email=models.EmailField(max_length=30,default="abc@gmail.com")
    Address=models.TextField(max_length=200,default="xyz ")
    bonus_points = models.IntegerField(default=0)


    def __str__(self):
        return self.user.username

# Menu model for different menu categories (e.g., Beverages, Starters)
class Menu(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='meals/', blank=False, null=False)

    def __str__(self):
        return self.name

# Dish model with an image field for food items under different menus
class Dish(models.Model):
    menu = models.ForeignKey(Menu, related_name='dishes', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='dishes/',  default='dishes/noodles.png',  blank=True, null=True)

    def __str__(self):
        return self.name


class TopProducts(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='top_products/', blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name

class Offer(models.Model):
    # dish = models.ForeignKey(Dish, related_name='offers', on_delete=models.CASCADE)
    # offer_price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00, blank=False, null=False)
    image = models.ImageField(upload_to='offers/')  # Requires Pillow for image processing
    description = models.TextField()
    # offer_price = models.DecimalField(max_digits=6, decimal_places=2)
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()

    def is_valid(self):
        """Check if the offer is still valid."""
        return self.valid_from <= timezone.now() <= self.valid_until

    def __str__(self):
        return f"Offer for {self.dish.name}"

    @classmethod
    def delete_expired_offers(cls):
        """Automatically delete expired offers."""
        cls.objects.filter(valid_until__lt=timezone.now()).delete()

# Cart model to manage user's cart with dynamic functionality

class userinfo(models.Model):
    username=models.CharField(max_length=50,default="abc")
    email=models.CharField(max_length=50,default="abc@gmail.com")

    def __str__(self):
        return self.username

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    def update_total_price(self):
        cart_items = self.cart_items.all()
        total = sum(item.get_total_price() for item in cart_items)
        self.total_price = total
        self.save()

    def __str__(self):
        return f"Cart for {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='cart_items', on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.SET_NULL, null=True, blank=True)
    offer = models.ForeignKey(Offer, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Add this line

    def get_total_price(self):
        if self.dish:
            return self.dish.price * self.quantity
        elif self.combo:
            return self.combo.price * self.quantity
        elif self.offer:
            discount_amount = (self.offer.discount_percentage / 100) * self.get_original_price()
            return (self.get_original_price() - discount_amount) * self.quantity
        return 0

    def get_original_price(self):
        total = 0
        if self.offer:
            total += sum(dish.price for dish in self.offer.dishes.all()) if self.offer.dishes.exists() else 0
            total += sum(combo.price for combo in self.offer.combos.all()) if self.offer.combos.exists() else 0
        return total

    def __str__(self):
        if self.dish:
            return f"{self.dish.name} (x{self.quantity})"
        elif self.combo:
            return f"{self.combo.name} (x{self.quantity})"
        elif self.offer:
            return f"{self.offer.name} (x{self.quantity})"
        return "Cart Item"


# Order model to handle orders and completion status

# Order model to store order details
class Order(models.Model):
    ORDER_MODE_CHOICES = [
        ('pickup', 'Pickup'),
        ('delivery', 'Delivery'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]

    user = models.ForeignKey(userinfo, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Field to store whether the user chose pickup or delivery
    order_mode = models.CharField(max_length=10, choices=ORDER_MODE_CHOICES, default='pickup')
    
    # Address field to store the delivery address, if 'delivery' is selected
    address = models.CharField(max_length=255, blank=True, null=True)  # Only for delivery mode
    
    # Date when the order was placed
    order_date = models.DateTimeField(auto_now_add=True)
    
    # Field to store the status of the order (Pending or Completed)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}, Mode: {self.order_mode}, Status: {self.status}"

    # Check if the order is for delivery
    def is_delivery(self):
        return self.order_mode == 'delivery'

    # Check if the order is for pickup
    def is_pickup(self):
        return self.order_mode == 'pickup'
    

    def mark_as_completed(self):
        if self.status == 'completed':
            user_copy = UserCopy.objects.get(username=self.user)
            user_copy.bonus_points += 1  # Increase the bonus points by 1
            user_copy.save()

    def save(self, *args, **kwargs):
        # If the order is being marked as completed, update bonus points
        if self.status == 'completed':
            self.mark_as_completed()
        super().save(*args, **kwargs)


class Offers(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='offers/')
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.title

# OrderItem model to track the items ordered in a particular order
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    dish = models.ForeignKey('Dish', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return self.quantity * self.dish.price

    def __str__(self):
        return f"{self.quantity} x {self.dish.name}"




class DeliverySettings(models.Model):
    restaurant_lat = models.FloatField()  # Latitude of the restaurant
    restaurant_lng = models.FloatField()  # Longitude of the restaurant
    delivery_radius = models.FloatField(help_text="Delivery radius in kilometers")

    def __str__(self):
        return f"Delivery radius: {self.delivery_radius} km"
    


class Gallery(models.Model):
    name = models.CharField(max_length=100, help_text="Enter the name of the image")
    image = models.ImageField(upload_to='gallery_images/', help_text="Upload an image")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name