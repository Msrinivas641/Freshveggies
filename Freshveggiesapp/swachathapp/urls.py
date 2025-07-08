# swachathapp/urls.py
from django.urls import path
from swachathapp import views 
from .views import add_to_cart, cart_view, remove_from_cart, update_cart,checkout, order, add_address,place_order,update_order_status, cancel_order, profile
from . import views  
from authcart import views as twoviews

urlpatterns = [
    path('', views.index, name="index"),
    path('index.html', views.index, name='index_html'),
    path('contact.html', views.contact, name="contact"),
    path('about', views.about, name="about"),
    path('login/',twoviews.handlelogin,name='handlelogin'),
    path('signup/',views.signup,name='signup'),
    path('logout', views.logout, name="logout"),
    path('vegetables.html', views.vegetable_view, name="vegetable"),
    path('leafyvegetables.html', views.leafyvegetable_view, name="leafyvegetables"),
    path('add-to-cart/<int:vegetable_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/',cart_view, name="cart"),
    path('update-cart/<int:cart_item_id>/<str:action>/', update_cart, name='update_cart'),
    path('remove-from-cart/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart'),
    path('checkout/', checkout, name='checkout'),
    path('order/', order, name='order'),
    path('add-address/', add_address, name='add_address'),
    path('place-order/', place_order, name='place_order'),
    path("update-order/<int:order_id>/", update_order_status, name="update_order"),
    path("cancel-order/<int:order_id>/", cancel_order, name="cancel_order"),
    path("profile.html", profile, name="profile"),
    path('delete/<int:order_id>/', views.delete_order, name='delete_order'),  # Add this line
]


    


