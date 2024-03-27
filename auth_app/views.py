from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_safe

@require_safe
def login_view(request):
    return HttpResponse("Login Page")
@require_safe
def signup_view(request):
    return HttpResponse("Signup Page")
@require_safe
def profile_view(request):
    return HttpResponse("Profile Page")