from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render 
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.db.models import Q

from website.helpers import scilab_run
from website.models import TextbookCompanionPreference,\
    TextbookCompanionProposal, TextbookCompanionChapter,\
    TextbookCompanionExample

def index(request):
    context = {}
    context.update(csrf(request))
    return render(request, 'website/templates/index.html', context)

@csrf_exempt
def ajax_books(request):
    context = {}
    if request.method == 'POST':
        category_id = request.POST['category_id']
        if category_id:
            ids = TextbookCompanionProposal.objects.using('scilab')\
                .filter(proposal_status=3).values('id')

            books = TextbookCompanionPreference.objects.using('scilab')\
                .filter(category=category_id).filter(approval_status=1)\
                .filter(proposal_id__in=ids).order_by('book')

            context = {
                'books': books
            }
    return render(request, 'website/templates/ajax-books.html', context)

@csrf_exempt
def ajax_chapters(request):
    context = {}
    if request.method == "POST":
        book_id = request.POST['book_id']
        if book_id:
            chapters = TextbookCompanionChapter.objects.using('scilab')\
                .filter(preference_id=book_id).order_by('number')

            context = {
                'chapters': chapters
            }
    return render(request, 'website/templates/ajax-chapters.html', context)

@csrf_exempt
def ajax_examples(request):
    context = {}
    if request.method == "POST":
        chapter_id = request.POST['chapter_id']
        if chapter_id:
            examples = TextbookCompanionExample.objects.using('scilab')\
                .filter(chapter_id=chapter_id).order_by('number')

            context = {
                'examples': examples
            }
    return render(request, 'website/templates/ajax-examples.html', context)

def ajax_execute(request):
    if request.method == "POST":
        code = request.POST['code']
        token = request.POST['csrfmiddlewaretoken']
        result = scilab_run(code, token)
        return HttpResponse(result)
