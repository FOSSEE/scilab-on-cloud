from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from django.forms.models import model_to_dict
from django.utils import simplejson
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core import serializers

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
from website.models import (TextbookCompanionCategoryList, ScilabCloudComment,
                            TextbookCompanionSubCategoryList,
                            TextbookCompanionProposal, TextbookCompanionChapter,
                            TextbookCompanionPreference,
                            TextbookCompanionExample,
                            TextbookCompanionExampleFiles,
                            TextbookCompanionRevision,
                            TextbookCompanionExampleDependency,
                            TextbookCompanionDependencyFiles,
                            TextbookCompanionExampleViews)
from website.forms import BugForm, RevisionForm
from website.dataentry import entry
from website.forms import issues

import base64
import utils
import json


def remove_from_session(request, keys):
    for key in keys:
        request.session.pop(key, None)


def subcategories(request):
    context = {}
    response_dict = []
    if request.is_ajax():
        maincategory_id = int(request.GET.get('maincat_id'))
        if maincategory_id:
            request.session['maincat_id'] = maincategory_id
            subcategory = TextbookCompanionSubCategoryList.objects.using('scilab')\
                .filter(maincategory_id=maincategory_id)

            for obj in subcategory:
                response = {
                    'subcategory': obj.subcategory,
                    'subcategory_id': obj.subcategory_id,
                }
                response_dict.append(response)
            return HttpResponse(simplejson.dumps(response_dict),
                                content_type='application/json')


def books(request):
    context = {}
    response_dict = []
    if request.is_ajax():
        main_category_id = int(request.GET.get('maincat_id'))
        category_id = int(request.GET.get('cat_id'))

        if category_id:
            # store category_id in cookie/session
            request.session['subcategory_id'] = category_id
            request.session['maincat_id'] = main_category_id
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
           # books = TextbookCompanionPreference.objects.using('scilab')\
           #     .filter(category=category_id).filter(approval_status=1)\
           #     .filter(cloud_pref_err_status=0)\
           #     .filter(proposal_id__in=ids).order_by('book')

            books = TextbookCompanionPreference.objects\
                .db_manager('scilab').raw("""
                        SELECT DISTINCT (loc.category_id),pe.id,
                        tcbm.sub_category,loc.maincategory, pe.book as book,
                        pe.author as author, pe.publisher as publisher,
                        pe.year as year, pe.id as pe_id, pe.edition,
                        po.approval_date as approval_date
                        FROM textbook_companion_preference pe LEFT JOIN
                        textbook_companion_proposal po ON pe.proposal_id = po.id
                        LEFT JOIN textbook_companion_book_main_subcategories
                        tcbm ON pe.id = tcbm.pref_id LEFT JOIN list_of_category
                        loc ON tcbm.main_category = loc.category_id WHERE
                        po.proposal_status = 3 AND pe.approval_status = 1
                        AND pe.category>0 AND pe.id = tcbm.pref_id AND
                        loc.category_id= %s AND tcbm.sub_category = %s""",
                                          [main_category_id, category_id])

            for obj in books:
                response = {
                    'book': obj.book,
                    'id': obj.id,
                    'author': obj.author
                }

                response_dict.append(response)
            return HttpResponse(simplejson.dumps(response_dict),
                                content_type='application/json')


def chapters(request):
    context = {}
    response_dict = []
    if request.is_ajax():
        book_id = int(request.GET.get('book_id'))
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
            for obj in chapters:
                response = {
                    'id': obj.id,
                    'number': obj.number,
                    'chapter': obj.name,

                }
                print obj.name
                response_dict.append(response)
            return HttpResponse(simplejson.dumps(response_dict),
                                content_type='application/json')


def examples(request):
    context = {}
    response_dict = []
    if request.is_ajax():
        chapter_id = int(request.GET.get('chapter_id'))
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
            for obj in examples:
                response = {
                    'id': obj.id,
                    'number': obj.number,
                    'caption': obj.caption,
                }
                print obj.caption
                response_dict.append(response)
            return HttpResponse(simplejson.dumps(response_dict),
                                content_type='application/json')


def revisions(request):
    commits = {}
    response_dict = []
    if request.is_ajax():
        example_id = int(request.GET.get('example_id'))
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
        print commits
        response = {
            'commits': commits
        }
        response_dict.append(response)
        return HttpResponse(simplejson.dumps(response),
                            content_type='application/json')


def code(request):
    commits = {}
    response_dict = []
    if request.is_ajax():
        commit_sha = request.GET.get('commit_sha')
        request.session['commit_sha'] = commit_sha
        remove_from_session(request, [
            'code',
        ])

        code = ''
        review = ''
        review_url = ''
        example_id = request.session['example_id']
        if not example_id:
            example_id = int(request.GET.get('example_id'))
        file_path = request.session['filepath']
        review = ScilabCloudComment.objects.using('scilab')\
            .filter(example=example_id).count()
        review_url = "http://scilab.in/cloud_comments/" + str(example_id)
        # example_path = UPLOADS_PATH + '/' + file_path

        file = utils.get_file(file_path, commit_sha, main_repo=True)
        code = base64.b64decode(file['content'])
        response = {
            'code': code,
            'review': review,
            'review_url': review_url
        }
        response_dict.append(response)
        return HttpResponse(simplejson.dumps(response),
                            content_type='application/json')


def contributor(request):
    context = {}
    contributor = {}
    response_dict = []
    if request.is_ajax():
        book_id = int(request.GET.get('book_id'))

        contributor = TextbookCompanionPreference.objects\
            .db_manager('scilab').raw("""SELECT preference.id,
            preference.book as preference_book,
            preference.author as preference_author,
            preference.isbn as preference_isbn,
            preference.publisher as preference_publisher,
            preference.edition as preference_edition,
            preference.year as preference_year,
            proposal.full_name as proposal_full_name,
            proposal.faculty as proposal_faculty,
            proposal.reviewer as proposal_reviewer,
            proposal.course as proposal_course,
            proposal.branch as proposal_branch,
            proposal.university as proposal_university
            FROM textbook_companion_proposal proposal
            LEFT JOIN textbook_companion_preference preference ON proposal.id =
            preference.proposal_id WHERE preference.id=%s""", [book_id])

        for obj in contributor:
            response = {
                "contributor_name": obj.proposal_full_name,
                "proposal_faculty": obj.proposal_faculty,
                "proposal_reviewer": obj.proposal_reviewer,
                "proposal_university": obj.proposal_university,
            }
            response_dict.append(response)
    return HttpResponse(simplejson.dumps(response),
                        content_type='application/json')


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
        dajax.redirect('?eid=' + ex_id, delay=1000)

    else:
        dajax.remove_css_class('#bug-form input', 'error')
        dajax.remove_css_class('#bug-form select', 'error')
        dajax.remove_css_class('#bug-form textarea', 'error')
        dajax.remove('.error-message')
        for error in form.errors:
            dajax.add_css_class('#id_{0}'.format(error), 'error')
        for field in form:
            for error in field.errors:
                message = '<div class="error-message">* {0}</div>'.format(
                    error)
                dajax.append('#id_{0}_wrapper'.format(field.name), 'innerHTML',
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
        data = render_to_string(
            'website/templates/submit-revision-error.html', context)
        dajax.assign('#submit-revision-wrapper', 'innerHTML', data)
        return dajax.json()

    if not request.user.is_anonymous():
        if 'commit_sha' not in request.session:
            context = {
                'error_message': 'Please select a revision',
            }
            data = render_to_string(
                'website/templates/submit-revision-error.html', context)
            dajax.assign('#submit-revision-wrapper', 'innerHTML', data)
            return dajax.json()

        form = RevisionForm()
        context = {'form': form}
        context.update(csrf(request))
        data = render_to_string(
            'website/templates/submit-revision.html', context)
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
    data = render_to_string(
        'website/templates/submit-revision-error.html', context)
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

            dajax.alert(
                'submitted successfully! \nYour changes will be visible after review.')
            dajax.script('$("#submit-revision-wrapper").trigger("close")')
    else:
        for error in form.errors:
            dajax.add_css_class('#id_{0}'.format(error), 'error')
        for field in form:
            for error in field.errors:
                message = '<div class="error-message">* {0}</div>'.format(
                    error)
                dajax.append('#id_{0}_wrapper'.format(
                    field.name), 'innerHTML', message)
        # non field errors
        if form.non_field_errors():
            message = '<div class="error-message"><small>{0}</small></div>'.format(
                form.non_field_errors())
            dajax.append('#non-field-errors', 'innerHTML', message)

    return dajax.json()


def diff(request):
    if request.is_ajax():
        diff_commit_sha = request.GET.get('diff_commit_sha')
        editor_code = request.GET.get('editor_code')
    context = {}
    file_path = request.session['filepath']
    file = utils.get_file(file_path, diff_commit_sha, main_repo=True)
    code = base64.b64decode(file['content'])
    response = {
        'code2': code,
    }
    return HttpResponse(simplejson.dumps(response),
                        content_type='application/json')

# ------------------------------------------------------------
# review interface functions


@dajaxice_register
def review_revision(request, revision_id):
    revision = TextbookCompanionRevision.objects.using(
        'scilab').get(id=revision_id)
    file = utils.get_file(revision.example_file.filepath,
                          revision.commit_sha, main_repo=False)
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
    revision = TextbookCompanionRevision.objects.using(
        'scilab').get(id=request.session['revision_id'])

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
    TextbookCompanionRevision.objects.using('scilab').get(
        id=request.session['revision_id']).delete()

    dajax.alert('removed successfully!')
    dajax.script('location.reload()')

    return dajax.json()
