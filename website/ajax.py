from dajax.core import Dajax
from django.utils import simplejson
from dajaxice.decorators import dajaxice_register

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render 
from django.template.loader import render_to_string
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.db.models import Q

from website.helpers import scilab_run
from website.models import TextbookCompanionPreference,\
    TextbookCompanionProposal, TextbookCompanionChapter,\
    TextbookCompanionExample, TextbookCompanionExampleFiles,\
    TextbookCompanionExampleDependency, TextbookCompanionDependencyFiles

@dajaxice_register
def books(request, category_id):
    dajax = Dajax()
    context = {}
    if category_id:
        ids = TextbookCompanionProposal.objects.using('scilab')\
            .filter(proposal_status=3).values('id')
        
        books = TextbookCompanionPreference.objects.using('scilab')\
            .filter(category=category_id).filter(approval_status=1)\
            .filter(proposal_id__in=ids).order_by('book')
        
        context = {
            'books': books
        }
    books = render_to_string('website/templates/ajax-books.html', context)
    dajax.assign('#books-wrapper', 'innerHTML', books)
    return dajax.json()

@dajaxice_register
def chapters(request, book_id):
    dajax = Dajax()
    context = {}
    if book_id:
        chapters = TextbookCompanionChapter.objects.using('scilab')\
            .filter(preference_id=book_id).order_by('number')

        context = {
            'chapters': chapters
        }
    chapters = render_to_string('website/templates/ajax-chapters.html', context)
    dajax.assign('#chapters-wrapper', 'innerHTML', chapters)
    return dajax.json()

@dajaxice_register
def examples(request, chapter_id):
    dajax = Dajax()
    context = {}
    if chapter_id:
        examples = TextbookCompanionExample.objects.using('scilab')\
            .filter(chapter_id=chapter_id).order_by('number')
        
        context = {
            'examples': examples
        }
    examples = render_to_string('website/templates/ajax-examples.html', context)
    dajax.assign('#examples-wrapper', 'innerHTML', examples)
    return dajax.json()

@dajaxice_register
def code(request, example_id):
    example = TextbookCompanionExampleFiles.objects.using('scilab')\
        .get(example_id=example_id, filetype='S')
    example_path = '/var/www/scilab_in/uploads/' + example.filepath
    f = open(example_path)
    code = f.read()
    f.close()
    return simplejson.dumps({'code': code})

@dajaxice_register
def execute(request, token, code, book_id, chapter_id, example_id):
    dependency_exists = TextbookCompanionExampleDependency.objects.using('scilab')\
        .filter(example_id=example_id).exists()
    data = scilab_run(code, token, book_id, dependency_exists)
    return simplejson.dumps(data)

@dajaxice_register
def contributor(request, book_id):
    dajax = Dajax()
    preference = TextbookCompanionPreference.objects.using('scilab')\
        .get(id=book_id)
    proposal = TextbookCompanionProposal.objects.using('scilab')\
        .get(id=preference.proposal_id)
    context = {
        "preference": preference,
        "proposal": proposal,
    }
    contributor = render_to_string('website/templates/ajax-contributor.html', context)
    dajax.assign('#databox', 'innerHTML', contributor)
    return dajax.json()
