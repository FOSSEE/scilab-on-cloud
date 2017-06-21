from dajax.core import Dajax
from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render 
from django.template.loader import render_to_string
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.db.models import Q

from website.helpers import scilab_run
from website.models import TextbookCompanionPreference,\
    TextbookCompanionProposal, TextbookCompanionChapter, TextbookCompanionRevision,\
    TextbookCompanionExample, TextbookCompanionExampleFiles,\
    TextbookCompanionExampleDependency, TextbookCompanionDependencyFiles

from website.forms import BugForm, RevisionForm, RevisionErrorForm
from soc.config import UPLOADS_PATH

from github import Github
import base64

from utils import g, user, repo
import utils


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
def revisions(request, example_id):
    dajax = Dajax()
    print('revisions')
    example = TextbookCompanionExampleFiles.objects.using('scilab')\
        .get(example_id=example_id, filetype='S')

    revisions = repo.get_commits(path=example.filepath)
    request.session['filepath'] = example.filepath

    context = {'revisions': []}
    for commit in revisions:
        print(commit.sha)
        context['revisions'].append({'id': commit.sha})

    # TODO: show latest revision on selecting the example
    # file_path = request.session['filepath']
    # file = repo.get_file_contents(path=file_path, ref=context['revisions'][0]['id'])
    # code = base64.b64decode(file.content)

    context['code'] = code

    revisions = render_to_string('website/templates/ajax-revisions.html', context)
    dajax.assign('#revisions-wrapper', 'innerHTML', revisions)
    return dajax.json()

@dajaxice_register
def code(request, revision_id):
    file_path = request.session['filepath']
    file = repo.get_file_contents(path=file_path, ref=revision_id)
    request.session['sha'] = file.sha
    code = base64.b64decode(file.content)
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

@dajaxice_register
def node(request, key):
    dajax = Dajax()
    data = render_to_string("website/templates/node-{0}.html".format(key))
    dajax.assign('#databox', 'innerHTML', data)
    return dajax.json()

@dajaxice_register
def bug_form(request):
    dajax = Dajax()
    context = {}
    form = BugForm()
    context['form'] = BugForm()
    context.update(csrf(request))
    form = render_to_string('website/templates/bug-form.html', context)
    dajax.assign('#bug-form-wrapper', 'innerHTML', form)
    return dajax.json()

@dajaxice_register
def bug_form_submit(request, form):
    dajax = Dajax()
    form = BugForm(deserialize_form(form))
    if form.is_valid():
        dajax.remove_css_class('#bug-form input', 'error')
        dajax.remove_css_class('#bug-form select', 'error')
        dajax.remove_css_class('#bug-form textarea', 'error')
        dajax.remove('.error-message')
        dajax.alert('Forms valid')
    else:
        dajax.remove_css_class('#bug-form input', 'error')
        dajax.remove_css_class('#bug-form select', 'error')
        dajax.remove_css_class('#bug-form textarea', 'error')
        dajax.remove('.error-message')
        for error in form.errors:
            dajax.add_css_class('#id_{0}'.format(error), 'error')
        for field in form:
            for error in field.errors:
                message = '<div class="error-message">* {0}</div>'.format(error)
                dajax.append('#id_{0}_wrapper'.format(field.name), 'innerHTML', message) 
        # non field errors
        if form.non_field_errors():
            message = '<div class="error-message"><small>{0}</small></div>'.format(form.non_field_errors())
            dajax.append('#non-field-errors', 'innerHTML', message)
    return dajax.json()

# submit revision
@dajaxice_register
def revision_form(request):
    dajax = Dajax()
    form = RevisionForm()
    context = {'form': form}
    context.update(csrf(request))
    data = render_to_string('website/templates/submit-revision.html', context)
    dajax.assign('#submit-revision-wrapper', 'innerHTML', data)
    return dajax.json()

@dajaxice_register
def revision_form_submit(request, form, code):
    dajax = Dajax()
    form = RevisionForm(deserialize_form(form))

    dajax.remove_css_class('#revision-form textarea', 'error')
    dajax.remove('.error-message')

    if form.is_valid():

        # push changes to temp repo
        # update_file returns True if the push is success.
        file_update = utils.update_file(
            request.session['filepath'],
            form.cleaned_data['commit_message'],
            base64.b64encode(code), 
            request.session['sha'],
            [request.user.username, request.user.email]
            )

        if file_update:
            # everything is fine

            rev = TextbookCompanionRevision()

            dajax.alert('submitted successfully! \nYour changes will be visible after review.')
            dajax.script('$("#submit-revision-wrapper").trigger("close")')
    else:
        for error in form.errors:
            dajax.add_css_class('#id_{0}'.format(error), 'error')
        for field in form:
            for error in field.errors:
                message = '<div class="error-message">* {0}</div>'.format(error)
                dajax.append('#id_{0}_wrapper'.format(field.name), 'innerHTML', message) 
        # non field errors
        if form.non_field_errors():
            message = '<div class="error-message"><small>{0}</small></div>'.format(form.non_field_errors())
            dajax.append('#non-field-errors', 'innerHTML', message)

    return dajax.json()

@dajaxice_register
def revision_error(request):
    dajax = Dajax()
    data = render_to_string('website/templates/submit-revision-error.html', {})
    dajax.assign('#submit-revision-error-wrapper', 'innerHTML', data)
    return dajax.json()    


