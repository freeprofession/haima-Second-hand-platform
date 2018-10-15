from django.shortcuts import HttpResponse, render


def homepage(request):
    return render(request, 'homepage.html')
