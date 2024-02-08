from django.urls import path
from . import views
from .views import *



urlpatterns = [
    path('', views.home, name='home'),
    path("about/", views.about, name="about"),
    path("profile/", views.profile, name="profile"),

    path("user_register/", views.user_register, name="user_register"),
    path("user_login/", views.user_login, name="user_login"),
    path("user_logout/", views.user_logout, name="user_logout"),
    path("edit_profile/", views.edit_profile, name="edit_profile"),

    path("upload_fitpic/", UploadFitpic.as_view(), name="upload_fitpic"),

    path("ootd/", views.ootd, name="ootd"),
    path("browse_fits/", PostFeed.as_view(), name="browse_fits"),
    path("style_guide/", views.style_guide, name="style_guide"),
    
]