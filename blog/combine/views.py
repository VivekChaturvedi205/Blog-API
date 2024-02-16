from django.shortcuts import render

def home(request):
    return render(request,'auth-register-cover.html')

def login(request):
    return render(request,'auth-login-cover.html')
