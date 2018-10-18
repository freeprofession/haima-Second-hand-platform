from django.shortcuts import HttpResponse, render


def homepage(request):
    return render(request, 'homepage.html')


def login(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')


def user_center_info(request):
    return render(request, 'user_center_info.html')
