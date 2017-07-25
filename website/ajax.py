from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.mail import EmailMultiAlternatives
from django.core.context_processors import csrf
from django.utils import simplejson
from django.utils.html import strip_tags
from django.template.loader import render_to_string, get_template
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.db.models import Q
from textwrap import dedent
from soc.config import FROM_EMAIL, TO_EMAIL, CC_EMAIL, BCC_EMAIL
from soc.config import UPLOADS_PATH
from website.helpers import scilab_run
#modified code
from website.helpers import scilab_run_user
from website.views import catg
from website.models import *
from website.forms import BugForm
from website.dataentry import entry
from website.forms import issues

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
    print example_id
    if example_id != '0':
        example = TextbookCompanionExampleFiles.objects.using('scilab')\
                    .get(example_id=example_id, filetype='S')
        review = ScilabCloudComment.objects.using('scilab')\
                    .filter(example=example_id).count()
        review_url = "http://scilab.in/cloud_comments/" + example_id
        example_path = UPLOADS_PATH + '/' + example.filepath
        f = open(example_path)
        code = f.read()
        f.close()
    else:
        code = ''
        review = ''
        review_url = ''
    return simplejson.dumps({'code': code, 'review': review,'review_url':\
    review_url})

@dajaxice_register
def execute(request, token, code, book_id, chapter_id, example_id, category_id):
    dependency_exists = TextbookCompanionExampleDependency\
                        .objects.using('scilab').filter(example_id=example_id)\
                        .exists()
    # modified code
    dependency_exists = entry(code, example_id, dependency_exists)
    condition = token is 0 or book_id is 0 or example_id is 0 or chapter_id\
                 is 0 or category_id is 0
    #modified code
    if condition:
        data = scilab_run_user(code,token,dependency_exists)
        return simplejson.dumps(data)
    else:
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
    contributor = render_to_string('website/templates/ajax-contributor.html',\
                                  context
                                  )
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
def bug_form_submit(request, form, cat_id, book_id, chapter_id, ex_id):
    dajax = Dajax()
    form = BugForm(deserialize_form(form))
    if form.is_valid():
        dajax.remove_css_class('#bug-form input', 'error')
        dajax.remove_css_class('#bug-form select', 'error')
        dajax.remove_css_class('#bug-form textarea', 'error')
        dajax.remove('.error-message')
        comment = form.cleaned_data['description']
        error = form.cleaned_data['issue']
        email = form.cleaned_data['email']
        print(comment)
        comment_data = TextbookCompanionPreference.objects.db_manager('scilab')\
                .raw(dedent("""\
                SELECT 1 as id, tcp.book as book, tcp.author as author,
                tcp.publisher as publisher, tcp.year as year,
                tcp.category as category, tce.chapter_id,
                tcc.number AS chapter_no, tcc.name AS chapter_name,
                tce.number AS example_no, tce.caption AS example_caption
                FROM textbook_companion_preference tcp
                LEFT JOIN textbook_companion_chapter tcc ON
                tcp.id = tcc.preference_id LEFT JOIN textbook_companion_example
                tce ON tce.chapter_id = tcc.id WHERE tce.id = %s"""),[ex_id])
        book_name = comment_data[0].book
        book_author = comment_data[0].author
        book_publisher = comment_data[0].publisher
        chapter_number = comment_data[0].chapter_no
        chapter_name = comment_data[0].chapter_name
        example_number = comment_data[0].example_no
        example_caption = comment_data[0].example_caption
        all_cat = False
        category = catg(comment_data[0].category, all_cat)
        subcategory = 0
        error_int = int(error)
        error =  issues[error_int][1]
        context = {
            'category': category,
            'subcategory' : subcategory,
            'error' : error,
            'book' : book_name,
            'author' :  book_author,
            'publisher' : book_publisher,
            'chapter_name' : chapter_name,
            'chapter_no' : chapter_number,
            'example_id' : ex_id,
            'example_caption' : example_caption,
            'example_no' : example_number,
            'comment' : comment,
        }
        scilab_comment = ScilabCloudComment()
        scilab_comment.type = error_int
        scilab_comment.comment = comment
        scilab_comment.email = email
        scilab_comment.category = comment_data[0].category
        scilab_comment.books = book_id
        scilab_comment.chapter = chapter_id
        scilab_comment.example = ex_id
        scilab_comment.save(using='scilab')
        subject = "New Cloud Comment"
        message = render_to_string('website/templates/email.html', context)
        from_email = FROM_EMAIL
        to_email = TO_EMAIL
        cc_email = CC_EMAIL
        bcc_email = BCC_EMAIL
        #Send Emails to, cc, bcc
        msg = EmailMultiAlternatives(subject, message, from_email, [to_email],
                                    bcc=[bcc_email], cc=[cc_email]
                                    )
        msg.content_subtype = "html"
        msg.send()
        dajax.alert("Thank you for your feedback")
        dajax.redirect('/index?eid=' + ex_id, delay=1000)

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
                dajax.append('#id_{0}_wrapper'.format(field.name), 'innerHTML',\
                message)
        #non field errors
        if form.non_field_errors():
            message = '<div class="error-message"><small>{0}</small></div>'\
                        .format(form.non_field_errors())
            dajax.append('#non-field-errors', 'innerHTML', message)
    return dajax.json()
