from django.shortcuts import render, redirect, get_object_or_404
from .models import Vegetable, Cart,Order,OrderItem,Address
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ContactForm
from django.shortcuts import get_object_or_404, redirect,render
from django.http import JsonResponse
from .models import Order
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.urls import reverse

def index(request):
    return render(request, "index.html")

@login_required
def contact(request):
    return render(request, "contact.html")

def about(request):
    return render(request, "about.html")

def login_view(request):
        
        if request.user.is_authenticated:
            return redirect("index")
    
        if request.method == "POST":
                form = AuthenticationForm(request, data=request.POST)
                if form.is_valid():
                    user = form.get_user()
                    print(user)
                    login(request, user)
                    return redirect("index")  # Redirect to homepage after login
                else:
                    messages.error(request, "Invalid username or password.")
                    
        form = AuthenticationForm()
        return render(request, "login.html", {"form": form})



def logout_view(request):
        logout(request)  # Log the user out
        return redirect("index") #  Redirect to home after logout

@login_required
def vegetable_view(request):
    vegetables = Vegetable.objects.filter(category='vegetable')
    return render(request, 'vegetables.html', {'vegetables': vegetables})


@login_required
def leafyvegetable_view(request):
    leafy_vegetables = Vegetable.objects.filter(category='leafy')
    return render(request, 'leafyvegetables.html', {'leafy_vegetables': leafy_vegetables})



@csrf_exempt
def add_to_cart(request, vegetable_id):
      

    vegetable = get_object_or_404(Vegetable, id=vegetable_id)
    quantity = int(request.POST.get("quantity", 1))

    cart_item, created = Cart.objects.get_or_create(user=request.user, vegetable=vegetable)
    cart_item.quantity += quantity
    cart_item.save()

    return redirect("cart")

  

@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)
    

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
        })


@login_required
def update_cart(request, cart_item_id, action):
    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)

    if action == "increase":
        cart_item.quantity += 1
    elif action == "decrease" and cart_item.quantity > 1:
        cart_item.quantity -= 1

    cart_item.save()
    return redirect("cart")
   # return redirect('cart_view') 


@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)
    
    # Delete the cart item
    cart_item.delete()

    return redirect('cart_view')


@login_required
def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("contact_success")  # Redirect to a success page
    else:
        form = ContactForm()
    
    return render(request, "contact.html", {"form": form})



@login_required
def add_address(request):
    if request.method == "POST":
        street_address = request.POST['street_address']
        city = request.POST['city']
        state = request.POST['state']
        zipcode = request.POST['zipcode']
        country = request.POST['country']

        Address.objects.create(
            user=request.user,
            street_address=street_address,
            city=city,
            state=state,
            zipcode=zipcode,
            country=country
        )
        messages.success(request, "Address added successfully.")
        return redirect('place_order')
    
    return render(request, 'add_address.html')


@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('cart_view')

    address = Address.objects.filter(user=request.user).first()
    if not address:
        messages.error(request, "Please add an address first.")
        return redirect('add_address')

    order = Order.objects.create(user=request.user, address=address)

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            vegetable=item.vegetable,
            quantity=item.quantity,
            price=item.vegetable.price
        )

    cart_items.delete()
    messages.success(request, "Order placed successfully.")
    return redirect('order')

@login_required
def order(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")

    return render(request, "order.html", {"orders":orders})


@login_required
def place_order(request):
    cart_items = Cart.objects.filter(user=request.user)
    if request.method == "POST":
        address = request.POST.get("address")
        
        # Make sure the cart is not empty
        if not cart_items:
            messages.error(request, "Your cart is empty.")
            return redirect("cart_view")
        
        # Calculate the total price from the cart items
        total_price = sum(item.vegetable.price * item.quantity for item in cart_items)
        
       # Create the order (without items)
        order = Order.objects.create(
            user=request.user,
            total_price=total_price,
            address=address,
            status='Processing'
        )


        
        # Create OrderItems for each cart item
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                vegetable=item.vegetable,
                quantity=item.quantity,
                price=item.vegetable.price
            )

        
        # Clear the cart
        cart_items.delete()

        messages.success(request, "Order placed successfully!")
        return redirect("order")
    
    return render(request, "place_order.html")


def signup(request):
    if request.method == "POST":
        email = request.POST.get("email")
       # username = request.POST.get("email")
        password = request.POST.get("password")
        address = request.POST.get("address")

        # ✅ Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered. Please log in.")
            return redirect("signup")  # Or return to signup page with an error

        # ✅ Create new user
        user = User.objects.create_user(username=email, email=email, password=password, address=address)
        messages.success(request, "Account created successfully! Please log in.")
        return redirect("login")  # Redirect to login page after signup

    return render(request, "signup.html")
    

@login_required
def update_order_status(request, order_id):
    if request.method == "POST":
        order = get_object_or_404(Order, id=order_id)
        new_status = request.POST.get("status")

        if new_status in [ "processing", "delivered", "cancelled", "shipped"]:
            order.status = new_status
            order.save()
            return JsonResponse({"success": True, "new_status": order.get_status_display()})

    return JsonResponse({"success": False, "error": "Invalid request"})





def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.status not in ["Cancelled", "Completed"]:  # Prevent canceling completed orders
        order.status = "Cancelled"
        order.save()
        messages.success(request, "Your order has been cancelled successfully.")


    return redirect(reverse('order'))# Redirect back to the orders pag

def profile(request):
    return render(request, "profile.html")



def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Optionally, delete associated OrderItems
    order.items.all().delete()  # This is to delete all the items in the order
    
    # Delete the order
    order.delete()
    
    # Redirect to the order page
    return redirect('order_page')



@login_required
def profile(request):
    return render(request, 'profile.html', {'user': request.user})
