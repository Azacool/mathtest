from django.shortcuts import render
from .models import Avto

def main(request):
    cars = Avto.objects.all()
    return render(request, 'index.html', {'cars': cars})
