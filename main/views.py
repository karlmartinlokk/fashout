from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.http import HttpResponseRedirect, JsonResponse
import json
from django.views import View 
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy, reverse

from .forms import CreateUserForm, LoginUserForm, UpdateUserForm, UpdateProfilePicForm, CreatePostFormImage, CreatePostFormCaption, CreatePostFormPieces, CommentForm
from .models import Post, Comment, User, UserFollowing

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from os import listdir
import os.path
from os.path import isfile
from os.path import join
from random import choice

# -- navigation bar

def home(request):

    all_following = UserFollowing.objects.filter(follower=request.user).values_list('user', flat=True) #takes all the user ids where the follower is request.user
    following_posts = Post.objects.filter(author__in=all_following)

    def random_img():
        dir_path = os.path.join(settings.BASE_DIR, "media/user_posts")
        files = [
            pic for pic in listdir(dir_path)
            if isfile(join(dir_path, pic))
        ]
        return choice(files)
    

    random_image_ootd = random_img()
    random_image_browse_fits = random_img()
    random_image_style_guide = random_img()

    context = {
        "random_image_ootd": random_image_ootd,
        "random_image_browse_fits": random_image_browse_fits,
        "random_image_style_guide": random_image_style_guide,
        "following_posts": following_posts
    }
    
    return render(request, "main/home.html", context)


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

@login_required(login_url="user_login")
def user_logout(request):
    
    auth.logout(request)

    return redirect("user_login")



# -- profile view

@login_required(login_url="user_login")
def profile(request, username=None):
    if username is None: #because by default, the logged in user's username is None
        username = request.user.username
    user = get_object_or_404(User, username=username)
    user_posts = Post.objects.filter(author=user).order_by("-date")

    is_following = UserFollowing.objects.filter(user=user, follower=request.user).exists()
    follower_count = UserFollowing.objects.filter(user=user).count()
    following_count = UserFollowing.objects.filter(follower=user).count()

    context = {
        "user": user,
        "user_posts": user_posts,
        "is_following": is_following,
        "follower_count": follower_count,
        "following_count": following_count,
    }
    return render(request, "main/user/profile.html", context)

@login_required
def toggle_follow(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    current_user = request.user

    # check if the user is already following the target user
    follow_relation = UserFollowing.objects.filter(user=user_to_follow, follower=current_user)
    
    if follow_relation.exists():
        follow_relation.delete()
        action = 'unfollowed'
    else:
        UserFollowing.objects.create(user=user_to_follow, follower=current_user)
        action = 'followed'

    return JsonResponse({'status': 'success', 'action': action})


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
    



# homepage

def ootd(request):
    return render(request, "main/ootd.html")


# search bar

def user_search(request):
    query = request.GET.get("search_query")
    users = []

    if query:
        users = User.objects.filter(username__icontains=query) #filters users based on username (case-insensitive)

    return render(request, "main/user_search.html", {
        'query': query,
        'users': users,
    })

def user_search(request):
    search_query = request.GET.get("query", "")  # Get the query from GET parameters
    if search_query:
        users = User.objects.filter(username__icontains=search_query)[:5]
        user_list = []
        for user in users:
            profile_image_url = user.profile.profile_image.url if hasattr(user, 'profile') and user.profile.profile_image else '/media/default.jpg'
            user_list.append({
                "id": user.id,
                "username": user.username,
                "profile_image_url": profile_image_url,  # Add profile image URL here
            })
        
        return JsonResponse({"users": user_list})
    return JsonResponse({"users": []})



# -- browse fits // fitpic feed

class PostFeed(View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all().order_by("-date")

        context = {
            "post_list": posts,
        }

        return render(request, "main/browse_fits.html", context)



class UploadFitpic(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        step = int(request.GET.get('step', 1))

        image_form = CreatePostFormImage()
        caption_form = CreatePostFormCaption()
        pieces_form = CreatePostFormPieces()

        temp_file_name = request.session.get('temp_file_name')
        if temp_file_name:
            image_url = default_storage.url(temp_file_name)
        else:
            image_url = '/media/upload_fitpic_default.jpg'

        context = {
            "image_form": image_form,
            "caption_form": caption_form,
            "pieces_form": pieces_form,
            "step": step,
            "image_url": image_url,
        }

        return render(request, "main/upload_fitpic.html", context)

    def post(self, request, *args, **kwargs):
        tab = request.POST.get('tab', '')
        image_file = request.FILES.get('image', None)

        if tab == 'caption':
            caption_form = CreatePostFormCaption(request.POST)
            if caption_form.is_valid():
                request.session['step1_data'] = caption_form.cleaned_data
                if image_file:
                    temp_file_name = default_storage.save(
                        f"temp/{image_file.name}",
                        ContentFile(image_file.read())
                    )
                    request.session['temp_file_name'] = temp_file_name

                return JsonResponse({'success': True, 'next_tab': True})
            else:
                print("Caption form errors:", caption_form.errors)

        elif tab == 'pieces':
            form = CreatePostFormPieces(request.POST)
            if form.is_valid():
                step1_data = request.session.get('step1_data', {})
                merged_data = {**step1_data, **form.cleaned_data}

                temp_file_name = request.session.get('temp_file_name')
                if temp_file_name:
                    new_post = Post(image=temp_file_name, **merged_data)
                    new_post.author = request.user
                    new_post.save()

                    with default_storage.open(temp_file_name, 'rb') as f:
                        file_data = f.read()
                    final_file_name = default_storage.save(
                        f"user_posts/{os.path.basename(temp_file_name)}",
                        ContentFile(file_data)
                    )

                    new_post.image = final_file_name
                    new_post.save()

                    temp_file_path = default_storage.path(temp_file_name)
                    if os.path.exists(temp_file_path):
                        os.remove(temp_file_path)

                    request.session.pop('step1_data', None)
                    request.session.pop('temp_file_name', None)

                    return JsonResponse({'success': True, 'final_step': True})
            else:
                print("Pieces form errors:", form.errors)
                
        return JsonResponse({'success': False, 'errors': form.errors})






@login_required(login_url="user_login")
def like(request):
    if request.POST.get("action") == "post":
        result = ""
        id = int(request.POST.get("postid"))
        post = get_object_or_404(Post, id=id)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            post.like_count -= 1
            result = post.like_count
            post.save()
        else:
            post.likes.add(request.user)
            post.like_count += 1
            result = post.like_count
            post.save()

        context = {
            "result": result,
            "like_count": post.like_count,
        }

        print(result)
        return JsonResponse(context)
    
def post_view(request, pk):
    post = get_object_or_404(Post, pk=pk) # pk=primary_key, the unique key for every database object
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()
            return redirect('post_view', pk=post.pk)  # Redirect to avoid re-posting if user refreshes the page
    else:
        form = CommentForm()

    comments = Comment.objects.filter(post=post).order_by("-raw_date")

    context = {
        "post": post,
        "form": form,
        "comments": comments,
    }
    return render(request, "main/user/post_view.html", context)


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        if request.POST.get("action") == "delete":
            post.delete()
            return JsonResponse({"deleted": True})

        tab = request.POST.get("tab")

        if tab == "caption":
            caption_form = CreatePostFormCaption(request.POST, instance=post)
            if caption_form.is_valid():
                caption_form.save()
                return JsonResponse({"success": True, "next_tab": True})

        elif tab == "pieces":
            pieces_form = CreatePostFormPieces(request.POST, instance=post)
            if pieces_form.is_valid():
                pieces_form.save()
                return JsonResponse({"success": True, "final_step": True})

        return JsonResponse({"success": False, "error": "Invalid form submission"})

    else:
        caption_form = CreatePostFormCaption(instance=post)
        pieces_form = CreatePostFormPieces(instance=post)

    return render(request, "main/user/post_edit.html", {
        "post": post,
        "caption_form": caption_form,
        "pieces_form": pieces_form,
    })

def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    post_id = comment.post.id
    if request.method == "POST":
        comment.delete()
        return redirect("post_view", pk=post_id)

def style_guide(request):
    return render(request, "main/style_guide.html")


