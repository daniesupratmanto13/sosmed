from django.shortcuts import render


# own function and class


def index(request):
    return render(request, 'index_main.html')
