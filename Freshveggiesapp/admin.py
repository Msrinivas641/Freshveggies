from django.contrib import admin
# Register your models here.
from .models import Vegetable,Cart, Contact
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,Order, OrderItem, Address

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("address",)}), ('Additional Info', {'fields': ('phonenumber',)}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("address",  "phonenumber","password",)}),('Additional Info', {'fields': ('phonenumber',)}), )
    list_display = ('username', 'email', 'address',  'is_active','phonenumber',)

admin.site.register(CustomUser, CustomUserAdmin)



@admin.register(Vegetable)
class VegetableAdmin(admin.ModelAdmin):
    list_display = ('name', 'weight', 'price')
    list_filter = ('category',)




class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'vegetable', 'quantity', 'total_price')

    def product_name(self, obj):
        """Get the product name dynamically"""
        return obj.product.name

    def total_price(self, obj):
        """Calculate the total price dynamically"""
        return obj.total_price()

admin.site.register(Cart, CartAdmin)



@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at")
    search_fields = ("name", "email")



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'status','address', 'created_at')
    list_filter = ('status',)
    search_fields = ('user__username', 'status','address')
    ordering = ('-created_at',)
    list_editable = ('status',)  # Allows status updates directly from the admin list


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'vegetable', 'quantity', 'price']

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'street_address', 'city', 'state', 'zipcode']


