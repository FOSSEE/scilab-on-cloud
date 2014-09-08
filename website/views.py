from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render 
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.db.models import Q

from website.helpers import scilab_run
from website.models import TextbookCompanionPreference,\
    TextbookCompanionProposal, TextbookCompanionChapter,\
    TextbookCompanionExample, TextbookCompanionExampleFiles,\
    TextbookCompanionExampleDependency, TextbookCompanionDependencyFiles

def index(request):
    context = {}
    context.update(csrf(request))
    return render(request, 'website/templates/index.html', context)
