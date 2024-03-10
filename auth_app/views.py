from django.shortcuts import render
from django.http import HttpResponse

def login_view(request):
    return HttpResponse("Login Page")

def signup_view(request):
    return HttpResponse("Signup Page")

def profile_view(request):
    return HttpResponse("Profile Page")