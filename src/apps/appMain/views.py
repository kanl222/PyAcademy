from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import CreateView

def main_view(request):
    return render(request, 'main.html')