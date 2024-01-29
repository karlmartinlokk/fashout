from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import CreateUserForm, LoginUserForm

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

# -- navigation bar

def home(request):
    return render(request, "main/home.html")

def about(request):
    return render(request, "main/about.html")




# -- register an user

def user_register(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("user_login")

    context = {"form":form}

    return render(request, "main/user_register.html", context=context)



# -- login user

def user_login(request):
    form = LoginUserForm()

    if request.method == "POST":
        form = LoginUserForm(request, data=request.POST)

        if form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect("profile")

    context = {"form": form}
    return render(request, "main/user_login.html", context=context)

# -- logout user

def user_logout(request):
    
    auth.logout(request)

    return redirect("user_login")

# -- profile view

@login_required(login_url="user_login")
def profile(request):
    return render(request, "main/profile.html")


# homepage

def ootd(request):
    return render(request, "main/ootd.html")

def browse_fits(request):
    return render(request, "main/browse_fits.html")

def style_guide(request):
    return render(request, "main/style_guide.html")



