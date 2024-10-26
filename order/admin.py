from django.contrib import admin
from .models import *
from django import forms

admin.site.register(userinfo)

# Inline class for displaying order items within the order admin



class OfferAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at']
    search_fields = ['title']

admin.site.register(Offers, OfferAdmin)




# Register the OrderItem model to be displayed inline with the Order model
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1  # Number of empty fields for additional items
    readonly_fields = ('dish', 'quantity')  # Display the ordered items but don't allow editing from admin

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'order_mode', 'get_address', 'status', 'order_date')
    list_filter = ('status', 'order_mode', 'order_date')
    search_fields = ('user__username', 'status')

    # Add OrderItemInline to show the ordered items in the order view
    inlines = [OrderItemInline]

    # Method to display the address for delivery orders
    def get_address(self, obj):
        if obj.order_mode == 'delivery':
            return obj.address
        return 'N/A'  # If it's a pickup order, no address is needed
    get_address.short_description = 'Delivery Address'

    # Allow admin to mark orders as completed via actions
    actions = ['mark_as_completed']

    def mark_as_completed(self, request, queryset):
        for order in queryset:
            if order.status != 'completed':  # Only update if not already completed
                order.status = 'completed'
                order.mark_as_completed()  # Update bonus points
                order.save()  # Save the order
        self.message_user(request, "Selected orders have been marked as completed and bonus points updated.")
    mark_as_completed.short_description = 'Mark selected orders as Completed'


# Register the Order model with custom admin options
admin.site.register(Order, OrderAdmin)








# @admin.register(Offer)
# class OfferAdmin(admin.ModelAdmin):
#     list_display = ('dish', 'offer_price', 'valid_from', 'valid_until', 'is_valid')
#     list_filter = ('valid_from', 'valid_until')
#     search_fields = ('dish__name', 'description')

# @admin.register(Dish)
# class DishAdmin(admin.ModelAdmin):
#     list_display = ('name', 'price')
#     search_fields = ('name',)


# Admin for managing dishes under specific menus
@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ['name', 'menu', 'price', 'is_available']
    list_filter = ['menu', 'is_available']
    search_fields = ['name']


# Admin for Menu management
@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']


# Inline class for CartItem management
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1


# Admin for Cart management
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_price']
    search_fields = ['user__username']
    inlines = [CartItemInline]


# Admin for UserCopy management
@admin.register(UserCopy)
class UserCopyAdmin(admin.ModelAdmin):
    list_display = ['username', 'phone_number']
    search_fields = ['username', 'phone_number']


# Register OrderItem if you want it to be managed separately, though it's already included in OrderAdmin
admin.site.register(OrderItem)

# Register TopProducts
admin.site.register(TopProducts)






from django.contrib import admin
from .models import DeliverySettings

@admin.register(DeliverySettings)
class DeliverySettingsAdmin(admin.ModelAdmin):
    list_display = ['restaurant_lat', 'restaurant_lng', 'delivery_radius']



from django.contrib import admin
from .models import Gallery

class GalleryAdmin(admin.ModelAdmin):
    list_display = ('name', 'uploaded_at')
    search_fields = ('name',)

admin.site.register(Gallery, GalleryAdmin)

