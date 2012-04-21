from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout


def home(request):
    return render(request, 'core/home.html')


def logout(request):
    """Logs out user"""
    auth_logout(request)
    return redirect('/')
