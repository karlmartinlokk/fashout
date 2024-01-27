from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, "main/home.html")

def ootd(request):
    return render(request, "main/ootd.html")

def about(request):
    return render(request, "main/about.html")

def profile(request):
    return render(request, "main/profile.html")