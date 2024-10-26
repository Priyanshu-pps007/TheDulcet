"""
URL configuration for Dulchet project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from order import views
from order.views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),

    path('logout/',views.logout_user,name='logout'),
    path('home/', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('cart/', views.view_cart, name='view_cart'),  # View cart
    path('cart/add/<str:item_type>/<int:item_id>/', views.add_to_cart, name='add_to_cart'),  # Add items to cart (dish/combo/offer)
    path('cart/remove/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),  # Remove items from cart
    # path('cart/update/<int:cart_item_id>/<str:action>/', views.update_cart_quantity, name='update_cart_quantity'),  # Update quantity (increase/decrease)
    path('cart/update/<int:cart_item_id>/<str:action>/', views.update_cart_quantity, name='update_cart_quantity'),
    # path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    # path('about/<int:dish_id>/', views.about_dish, name='about_dish'),

    # path('delete-from-cart/<int:item_id>/', views.delete_from_cart, name='delete_from_cart'),
    path('meals/', views.meals, name='meals'),
    path('meals/<int:meal_id>/', views.dish, name='dish'),
    path('offers/', offers_view, name='offers'),

    path('about/dish/<int:dish_id>/', views.about_dish, name='about_dish'),
    path('about/combo/<int:combo_id>/', views.about_combo, name='about_combo'),


    #   path('about/<str:item_type>/<int:item_id>/', views.about_item, name='about_item'),
    path('cart/', views.view_cart, name='view_cart'),


    path('place_order/', views.place_order, name='place_order'),
    # path('order_confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),

       path('check-delivery/', check_delivery, name='check_delivery'),


    path('choose-order-type/', views.choose_order_type, name='choose_order_type'),
    path('place-order/', views.place_order, name='place_order'),
      path('account/', views.account_page, name='account_page'),
    #    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

     path('gallery/', views.gallery_view, name='gallery'),

]
if settings.DEBUG:  # This ensures static files are served only in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





