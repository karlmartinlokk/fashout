from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from django import forms
from django.forms.widgets import PasswordInput, TextInput

from .models import Profile, Post, Comment


# -- register user
class CreateUserForm(UserCreationForm): 

    username = forms.CharField(
        label='Username',
        widget=TextInput(),
        error_messages={
            'unique': 'This username is already taken. Please choose a different one.',
        }
    )
    email = forms.EmailField(
        label='Email',
        widget=TextInput(),
        error_messages={
            'unique': 'This email address is already registered. Please use a different one.',
        }
    )
    password1 = forms.CharField(
        label='Password',
        widget=PasswordInput(),
        error_messages={
            'password_mismatch': 'The two password fields didn’t match.',
        }
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=PasswordInput(),
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]




#-- login user
class LoginUserForm(AuthenticationForm):

    username = forms.CharField(
        label="",
        widget=TextInput(attrs={
            "placeholder": "username"
        }),
    )
    password = forms.CharField(
        label="",
        widget=PasswordInput(attrs={
            "placeholder": "password"
        }),
    )





# -- update user profile
class UpdateUserForm(forms.ModelForm):

    username = forms.CharField(
        label='',
        widget=TextInput(attrs={
            "placeholder": "username"
        }),
        error_messages={
            'unique': 'This username is already taken. Please choose a different one.',
        }
    )
    email = forms.EmailField(
        label='',
        widget=TextInput(attrs={
            "placeholder": "email"
        }),
        error_messages={
            'unique': 'This email address is already registered. Please use a different one.',
        }
    )

    class Meta:
        model = User
        fields = ["username", "email"]

class UpdateProfilePicForm(forms.ModelForm):

    profile_image = forms.ImageField(
        label=''
    )
    class Meta:
        model = Profile
        fields = ["profile_image"]



# -- create post form
        
class CreatePostFormImage(forms.ModelForm):
    image = forms.ImageField(
        label = "",
        widget = forms.ClearableFileInput(attrs={
            "class": "form_control_image",
    }))

    class Meta:
        model = Post
        fields = ["image"]

class CreatePostFormCaption(forms.ModelForm):
    
    caption = forms.CharField(
        label = "",
        max_length = 50,
        widget = forms.Textarea(attrs={
            "rows": "2",
            "placeholder" : "Add caption...",
            "class": "form_control_caption",
        }))
    
    def clean_caption(self):
            caption = self.cleaned_data.get('caption')
            if len(caption) > 50:
                raise forms.ValidationError("Caption length should not exceed 50 characters.")
            return caption

    class Meta:
        model = Post
        fields = ["caption"]

class CreatePostFormPieces(forms.ModelForm):
    
    caption = forms.CharField(
        label = "",
        max_length = 50,
        widget = forms.Textarea(attrs={
            "rows": "2",
            "placeholder" : "Add pieces...",
            "class": "form_control_caption",
        }))
    
    def clean_caption(self):
            caption = self.cleaned_data.get('caption')
            if len(caption) > 50:
                raise forms.ValidationError("Caption length should not exceed 50 characters.")
            return caption

    class Meta:
        model = Post
        fields = ["caption"]



# -- create comment form
        
class CommentForm(forms.ModelForm):

    caption = forms.CharField(
        label = "",
        max_length= 300,
        widget = forms.Textarea(attrs={
            "rows": "2",
            "placeholder" : "write a comment..."
        }))

    class Meta:
        model = Comment
        fields = ["caption"]