from django.shortcuts import render 
from django.core.context_processors import csrf
from website.models import *

def index(request):
    context = {}
    return render(request, 'website/templates/index.html', context)

def catg(cat_id):
    category = TextbookCompanionCategoryList.objects.using('scilab').get(id=cat_id)
    return category.category_name
