from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from django.forms.models import model_to_dict

# from django.http import HttpResponse, HttpResponseRedirect
# from django.shortcuts import render, redirect
from django.core.mail import EmailMultiAlternatives
from django.core.context_processors import csrf
from django.utils import simplejson
# from django.utils.html import strip_tags
from django.template.loader import render_to_string, get_template
# from django.views.decorators.csrf import csrf_exempt, csrf_protect
# from django.db.models import Q
from textwrap import dedent
from soc.config import FROM_EMAIL, TO_EMAIL, CC_EMAIL, BCC_EMAIL
from soc.config import UPLOADS_PATH
from website.helpers import scilab_run
# modified code
from website.helpers import scilab_run_user
from website.views import catg
from website.models import TextbookCompanionCategoryList, ScilabCloudComment,\
    TextbookCompanionSubCategoryList, TextbookCompanionProposal,\
    TextbookCompanionPreference, TextbookCompanionChapter,\
    TextbookCompanionExample, TextbookCompanionExampleFiles,\
    TextbookCompanionRevision, TextbookCompanionExampleDependency,\
    TextbookCompanionDependencyFiles
from website.forms import BugForm, RevisionForm
from website.dataentry import entry
from website.forms import issues

import base64
import utils
import json


def remove_from_session(request, keys):
    for key in keys:
        request.session.pop(key, None)


@dajaxice_register
def books(request, category_id):
    dajax = Dajax()
    context = {}

    if category_id:
        # store category_id in cookie/session
        request.session['category_id'] = category_id
        remove_from_session(request, [
            'book_id',
            'chapter_id',
            'example_id',
            'commit_sha',
            'example_file_id',
            'filepath',
            'code',
        ])

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
        request.session['book_id'] = book_id
        remove_from_session(request, [
            'chapter_id',
            'example_id',
            'commit_sha',
            'example_file_id',
            'filepath',
            'code',
        ])

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
        request.session['chapter_id'] = chapter_id
        remove_from_session(request, [
            'example_id',
            'commit_sha',
            'example_file_id',
            'filepath',
            'code',
        ])

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

    request.session['example_id'] = example_id
    remove_from_session(request, [
            'commit_sha',
            'example_file_id',
            'filepath',
            'code',
        ])

    example_file = TextbookCompanionExampleFiles.objects.using('scilab')\
        .get(example_id=example_id, filetype='S')

    request.session['example_file_id'] = example_file.id
    request.session['filepath'] = example_file.filepath

    commits = utils.get_commits(file_path=example_file.filepath)

    context = {
        'revisions': commits,
        'code': code,
    }

    revisions = render_to_string('website/templates/ajax-revisions.html', context)
    dajax.assign('#revisions-wrapper', 'innerHTML', revisions)
    return dajax.json()


@dajaxice_register
def code(request, commit_sha):

    request.session['commit_sha'] = commit_sha
    remove_from_session(request, [
                'code',
            ])

    code = ''
    review = ''
    review_url = ''
    example_id = request.session['example_id']
    file_path = request.session['filepath']
    review = ScilabCloudComment.objects.using('scilab')\
        .filter(example=example_id).count()
    review_url = "http://scilab.in/cloud_comments/" + str(example_id)
    # example_path = UPLOADS_PATH + '/' + file_path

    file = utils.get_file(file_path, commit_sha, main_repo=True)
    code = base64.b64decode(file['content'])
    return simplejson.dumps({
        'code': code,
        'review': review,
        'review_url': review_url
    })


@dajaxice_register
def execute(request, token, code, book_id, chapter_id, example_id, category_id):
    dependency_exists = TextbookCompanionExampleDependency\
                        .objects.using('scilab').filter(example_id=example_id)\
                        .exists()
    # modified code
    dependency_exists = entry(code, example_id, dependency_exists, book_id)
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
    contributor = render_to_string(
        'website/templates/ajax-contributor.html',
        context)
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
                tce ON tce.chapter_id = tcc.id WHERE tce.id = %s"""), [ex_id])
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
        error = issues[error_int][1]
        context = {
            'category': category,
            'subcategory': subcategory,
            'error': error,
            'book': book_name,
            'author':  book_author,
            'publisher': book_publisher,
            'chapter_name': chapter_name,
            'chapter_no': chapter_number,
            'example_id': ex_id,
            'example_caption': example_caption,
            'example_no': example_number,
            'comment': comment,
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
        # Send Emails to, cc, bcc
        msg = EmailMultiAlternatives(
                        subject,
                        message,
                        from_email,
                        [to_email],
                        bcc=[bcc_email],
                        cc=[cc_email]
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
        # non field errors
        if form.non_field_errors():
            message = '<div class="error-message"><small>{0}</small></div>'\
                        .format(form.non_field_errors())
            dajax.append('#non-field-errors', 'innerHTML', message)
    return dajax.json()


# submit revision
@dajaxice_register
def revision_form(request, code, initial_code):
    dajax = Dajax()
    request.session['code'] = code

    if code == initial_code:
        context = {
            'error_message': 'You have not made any changes',
        }
        data = render_to_string('website/templates/submit-revision-error.html', context)
        dajax.assign('#submit-revision-wrapper', 'innerHTML', data)
        return dajax.json()

    if not request.user.is_anonymous():
        if 'commit_sha' not in request.session:
            context = {
                'error_message': 'Please select a revision',
            }
            data = render_to_string('website/templates/submit-revision-error.html', context)
            dajax.assign('#submit-revision-wrapper', 'innerHTML', data)
            return dajax.json()

        form = RevisionForm()
        context = {'form': form}
        context.update(csrf(request))
        data = render_to_string('website/templates/submit-revision.html', context)
    else:
        data = render_to_string('website/templates/revision-login.html', {})
    dajax.assign('#submit-revision-wrapper', 'innerHTML', data)
    return dajax.json()


@dajaxice_register
def revision_error(request):
    dajax = Dajax()
    context = {
        'error_message': 'You have not made any changes',
    }
    data = render_to_string('website/templates/submit-revision-error.html', context)
    dajax.assign('#submit-revision-error-wrapper', 'innerHTML', data)
    return dajax.json()


@dajaxice_register
def revision_form_submit(request, form, code):
    dajax = Dajax()
    form = RevisionForm(deserialize_form(form))

    dajax.remove_css_class('#revision-form textarea', 'error')
    dajax.remove('.error-message')

    if form.is_valid():

        commit_message = form.cleaned_data['commit_message']
        username, email = request.user.username, request.user.email

        # push changes to temp repo
        # update_file returns True if the push is success.
        commit_sha = utils.update_file(
            request.session['filepath'],
            commit_message,
            base64.b64encode(code),
            [username, email],
            main_repo=False,
            )

        if commit_sha is not None:
            # everything is fine

            # save the revision info in database
            rev = TextbookCompanionRevision(
                    example_file_id=request.session['example_file_id'],
                    commit_sha=commit_sha,
                    commit_message=commit_message,
                    committer_name=username,
                    committer_email=email,
                )
            rev.save(using='scilab')

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
def diff(request, diff_commit_sha, editor_code):
    dajax = Dajax()
    context = {}
    file_path = request.session['filepath']
    file = utils.get_file(file_path, diff_commit_sha, main_repo=True)
    code = base64.b64decode(file['content'])
    page = render_to_string('website/templates/diff.html', context)
    dajax.assign('#diff-wrapper', 'innerHTML', page)

    data = {
        'dajax': json.loads(dajax.json()),
        'code2': code,
    }

    return simplejson.dumps(data)

# ------------------------------------------------------------
# review interface functions


@dajaxice_register
def review_revision(request, revision_id):
    revision = TextbookCompanionRevision.objects.using('scilab').get(id=revision_id)
    file = utils.get_file(revision.example_file.filepath, revision.commit_sha, main_repo=False)
    code = base64.b64decode(file['content'])

    request.session['revision_id'] = revision_id

    example = revision.example_file.example
    chapter = example.chapter
    book = chapter.preference
    category = utils.get_category(book.category)

    data = {
        'code': code,
        'revision': model_to_dict(revision),
        'example': model_to_dict(example),
        'chapter': model_to_dict(chapter),
        'book': model_to_dict(book),
        'category': category,
        'createdAt': str(revision.timestamp),
    }
    return simplejson.dumps(data)


@dajaxice_register
def push_revision(request, code):
    """
    code: from code editor on review interface
    """
    dajax = Dajax()
    revision = TextbookCompanionRevision.objects.using('scilab').get(id=request.session['revision_id'])

    print('pushing to repo')
    utils.update_file(
        revision.example_file.filepath,
        revision.commit_message,
        base64.b64encode(code),
        [revision.committer_name, revision.committer_email],
        branch='master',
        main_repo=True)

    print('update push_status')
    revision.push_status = True
    revision.save()

    dajax.alert('pushed successfully!')
    dajax.script('location.reload()')

    return dajax.json()


@dajaxice_register
def remove_revision(request):
    """
    remove revision from revision database
    """
    dajax = Dajax()
    print(request.session['revision_id'])
    TextbookCompanionRevision.objects.using('scilab').get(id=request.session['revision_id']).delete()

    dajax.alert('removed successfully!')
    dajax.script('location.reload()')

    return dajax.json()
