from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.http import HttpResponseRedirect, JsonResponse
from django.views import View 
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy, reverse

from .forms import CreateUserForm, LoginUserForm, UpdateUserForm, UpdateProfilePicForm, CreatePostFormImage, CreatePostFormCaption, CreatePostFormPieces, CommentForm
from .models import Post, Comment, User

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

    context = {
        "user": user,
        "user_posts": user_posts,
    }
    return render(request, "main/user/profile.html", context)



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

def search(request):
    return render(request, "main/search.html")


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

        # Retrieve the uploaded image from the session if it exists
        image_url = request.session.get('image_url', '/media/upload_fitpic_default.jpg')

        context = {
            "image_form": image_form,
            "caption_form": caption_form,
            "pieces_form": pieces_form,
            "step": step,
            "image_url": image_url,
        }

        return render(request, "main/upload_fitpic.html", context)

    def post(self, request, *args, **kwargs):
        step = int(request.POST.get('step', 1))

        if step == 1:
            image_form = CreatePostFormImage(request.POST, request.FILES)
            if image_form.is_valid():
                # Get the uploaded image from the form
                image = request.FILES.get('image')

                # Save the image temporarily
                temp_file_name = default_storage.save(f"temp/{image.name}", ContentFile(image.read()))
                temp_file_path = default_storage.path(temp_file_name)
                file_url = default_storage.url(temp_file_name)

                # Store the file path in the session
                request.session['image_url'] = file_url

                caption_form = CreatePostFormCaption(request.POST)
                if caption_form.is_valid():
                    request.session['step1_data'] = caption_form.cleaned_data
                    return JsonResponse({'success': True, 'next_step': 2})

        elif step == 2:
            form = CreatePostFormPieces(request.POST, request.FILES)
            if form.is_valid():
                step1_data = request.session.get('step1_data', {})
                merged_data = {**step1_data, **form.cleaned_data}

                # Retrieve the stored image URL from the session
                image_url = request.session.get('image_url')
                if image_url:
                    # Save the image path to the post model
                    new_post = Post(image=image_url, **merged_data)
                    new_post.author = request.user
                    new_post.save()

                    # Cleanup: Move the image to the final directory
                    final_file_name = f"user_posts/{image.name}"
                    final_file_path = default_storage.save(final_file_name, ContentFile(image.read()))

                    # Delete the temporary file
                    if os.path.exists(temp_file_path):
                        os.remove(temp_file_path)

                    # Clear the session
                    request.session.pop('step1_data', None)
                    request.session.pop('image_url', None)

                    return JsonResponse({'success': True, 'final_step': True})

        return JsonResponse({'success': False})





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


class PostEditView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ["caption"]
    template_name = "main/user/post_edit.html"

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse_lazy("post_view", kwargs={"pk": pk})

    def post(self, request, *args, **kwargs):
        action = request.POST.get("action")
        if action == "save":
            return super().post(request, *args, **kwargs)
        elif action == "delete":
            return redirect("post_delete_confirmation", pk=self.kwargs["pk"])

class PostDeleteConfirmation(DeleteView):
    model = Post
    template_name = "main/user/post_delete_confirmation.html"
    success_url = reverse_lazy("profile")

    def delete(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            return redirect(self.success_url)
        
        if "confirm" in request.POST:
            post = self.get_object()
            image_path = os.path.join(settings.MEDIA_ROOT, 'user_posts', str(post.image)) #should delete image from folder "user_posts"
            if os.path.exists(image_path):
                os.remove(image_path)
            return super().delete(request, *args, **kwargs)

        return redirect(self.success_url)

def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    post_id = comment.post.id
    if request.method == "POST":
        comment.delete()
        return redirect("post_view", pk=post_id)

def style_guide(request):
    return render(request, "main/style_guide.html")



