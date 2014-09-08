from django.shortcuts import render 
from django.core.context_processors import csrf

def index(request):
    context = {}
    context.update(csrf(request))
    return render(request, 'website/templates/index.html', context)
