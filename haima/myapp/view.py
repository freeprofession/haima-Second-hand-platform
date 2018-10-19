from django.shortcuts import HttpResponse, render


def homepage(request):
    return render(request, 'homepage.html')


def login(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')


def user_center_info(request):
    return render(request, 'user_center_info.html')


def publish(request):
    return render(request, 'publish.html')


def auction(request):
    return render(request, 'auction-index.html')


def sale(request):
    return render(request, 'sale.html')


def buy(request):
    return render(request, 'buy.html')


def address(request):
    return render(request, 'address.html')
