from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View

from .forms import CreateUserForm, LoginUserForm, UpdateUserForm, UpdateProfilePicForm, CreatePostForm
from .models import Post

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
    if request.method == "POST":
        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("user_login")

    else:
        form = CreateUserForm()

    context = {"form":form}
    return render(request, "main/user/user_register.html", context=context)



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
    return render(request, "main/user/user_login.html", context=context)

# -- logout user

def user_logout(request):
    
    auth.logout(request)

    return redirect("user_login")



# -- profile view

@login_required(login_url="user_login")
def profile(request):
    return render(request, "main/user/profile.html")



# -- edit profile

@login_required(login_url="user_login")
def edit_profile(request):
    if request.method == "POST":
        u_form = UpdateUserForm(request.POST, instance=request.user)
        p_form = UpdateProfilePicForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect("profile")

    else:
        u_form = UpdateUserForm(instance=request.user)
        p_form = UpdateProfilePicForm(instance=request.user.profile)

    context = {
        "u_form": u_form,
        "p_form": p_form,
    }

    return render(request, "main/user/edit_profile.html", context)
    


# -- upload fitpic
@login_required(login_url="user_login")
def upload_fitpic(request):
    return render(request, "main/fitpic_upload.html")






# homepage

def ootd(request):
    return render(request, "main/ootd.html")


# -- browse fits // fitpic feed

class PostFeed(View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all().order_by("-date")

        context = {
            "post_list": posts,
        }

        return render(request, "main/browse_fits.html", context)

class UploadFitpic(View):
    def get(self, request, *args, **kwargs):
        form = CreatePostForm()

        context = {
            "form": form,
        }

        return render(request, "main/upload_fitpic.html", context)

    def post(self, request, *args, **kwargs):
        form = CreatePostForm(request.POST, request.FILES)


        if form.is_valid():
            new_post = form.save(commit = False)
            new_post.author = request.user
            new_post.save()
            return redirect("profile")
        context = {
            "form": form,
        }
        
        return render(request, "main/upload_fitpic.html", context)

def style_guide(request):
    return render(request, "main/style_guide.html")



