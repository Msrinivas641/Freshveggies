from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from swachathapp.models import CustomUser
from django.contrib.auth import authenticate,login,logout



User = get_user_model()

def signup(request):
    if request.method == "POST":
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("pass1")
        address = request.POST.get("address")
        phonenumber = request.POST.get("phonenumber")

        print(f"Signup Attempt - Username: {username}, Password: {password}")


        # ✅ Check if email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "username is already registered. Please log in.")
            return redirect("signup")  # Or return to signup page with an error
        

        # ✅ Check if email is already registered
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered. Please log in.")
            return redirect("signup")  # Redirect to signup page with an error


        # ✅ Create new user
        user = CustomUser.objects.create_user(username=username, email=email, password=password, address=address,phonenumber=phonenumber,)

        user.save()
        messages.success(request, "Account created successfully! Please log in.")
        #return redirect( "login")  # Redirect to login page after signup

    return render(request, "signup.html")

class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        return HttpResponse("Account activation logic here")

 


def handlelogin(request):

    if request.method=='POST':
        username=request.POST.get("username")
        password=request.POST.get("pass1")

        print(username)
        print(password)


        user = authenticate(request, username=username, password=password)
        # ✅ Debugging: Print what authenticate() returns
        print(f"Authenticated User: {user}")

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful")
            return redirect("/")
        else:
            messages.error(request, "Invalid credentials")
            return redirect('/auth/login')
        
    return render(request, "login.html")





def handlelogout(request):
    logout(request)
    return redirect('/auth/login')
