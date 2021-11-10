from django.shortcuts import render, reverse
from django.http import HttpResponse


def index(request):
    return render(request, 'index.html')
