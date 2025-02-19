from django.urls import path
from . import views
from .views import *



urlpatterns = [
    path('', views.home, name='home'),

    path("about/", views.about, name="about"),

    path('profile/', views.profile, name='profile'),
    path("follow/<str:username>/", views.toggle_follow, name="toggle_follow"),
    path('profile/<str:username>/', views.profile, name='profile'),
    path("user_register/", views.user_register, name="user_register"),
    path("user_login/", views.user_login, name="user_login"),
    path("user_logout/", views.user_logout, name="user_logout"),
    path("edit_profile/", views.edit_profile, name="edit_profile"),
    path("upload_fitpic/", UploadFitpic.as_view(), name="upload_fitpic"),

    path('search-users/', views.user_search, name='user_search'),

    path("ootd/", views.ootd, name="ootd"),

    path("browse_fits/", PostFeed.as_view(), name="browse_fits"),

    path("<int:pk>/", views.post_view, name="post_view"),
    path("post_edit/<int:pk>/", views.post_edit, name="post_edit"),
    path('comment_delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path("like/", views.like, name="like"),

    path("style_guide/", views.style_guide, name="style_guide"),
    
]