from django.shortcuts import render 
from django.core.context_processors import csrf

def index(request):
    context = {}
    return render(request, 'website/templates/index.html', context)
