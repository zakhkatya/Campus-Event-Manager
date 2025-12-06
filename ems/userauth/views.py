from django.shortcuts import render

def auth_home(request):
    return render(request, "userauth/auth_home.html")