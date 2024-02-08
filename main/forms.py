from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from django import forms
from django.forms.widgets import PasswordInput, TextInput

from .models import Profile, Post


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

    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())





# -- update user profile
class UpdateUserForm(forms.ModelForm):

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

    class Meta:
        model = User
        fields = ["username", "email"]

class UpdateProfilePicForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["image"]



# -- create post form
        
class CreatePostForm(forms.ModelForm):
    
    caption = forms.CharField(
        label = "Label",
        widget = forms.Textarea(attrs={
            "rows": "2",
            "placeholder" : "Add caption..."
        }))
    
    image = forms.ImageField(required=False)

    class Meta:
        model = Post
        fields = ["image", "caption"]
