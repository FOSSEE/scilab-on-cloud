from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.contrib.auth import logout
from django.template import loader
import json as simplejson
from django.http import HttpResponse

from django.core import serializers
from django.db.models import F
from textwrap import dedent

from website.models import (TextbookCompanionCategoryList, ScilabCloudComment,
                            TextbookCompanionSubCategoryList,
                            TextbookCompanionProposal,
                            TextbookCompanionPreference,
                            TextbookCompanionChapter,
                            TextbookCompanionExample,
                            TextbookCompanionExampleFiles,
                            TextbookCompanionRevision,
                            TextbookCompanionExampleDependency,
                            TextbookCompanionDependencyFiles,
                            TextbookCompanionPreferenceHits,
                            TextbookCompanionExampleViews)
from soc.config import UPLOADS_PATH, GARUDA_SERVER
from . import utils
import base64
from collections import OrderedDict
from django.db.models import Q

def catg(cat_id, all_cat):
    if all_cat is False:
        category = TextbookCompanionCategoryList.objects.using('scilab')\
            .get(category_id=cat_id)
        return category.maincategory
    else:
        category = TextbookCompanionCategoryList.objects.using('scilab')\
            .filter(~Q(category_id=0)).order_by('maincategory')
        return category


def subcatg(subcat_id, all_subcat):
    if all_subcat is False:
        category = TextbookCompanionSubCategoryList.objects.using('scilab')\
            .get(id=subcat_id)
        return category.subcategory
    else:
        category = TextbookCompanionSubCategoryList.objects.using('scilab')\
            .all().order_by('subcategory')
        return category


def get_subcategories(maincat_id):
    subcategories = TextbookCompanionSubCategoryList.objects.using('scilab')\
        .filter(maincategory_id=maincat_id).order_by('subcategory_id')
    return subcategories


def get_books(category_id):

    books = TextbookCompanionPreference.objects\
        .db_manager('scilab').raw("""
                        SELECT DISTINCT (loc.category_id),pe.id,
                        tcbm.sub_category,loc.maincategory, pe.book as
                        book,loc.category_id,tcbm.sub_category,
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
                        pe.cloud_pref_err_status = 0 AND
                        tcbm.sub_category=%s""", [category_id])
    return books


def get_chapters(book_id):
    chapters = TextbookCompanionChapter.objects.using('scilab')\
        .filter(preference_id=book_id).filter(cloud_chapter_err_status=0)\
        .order_by('number')
    return chapters


def get_examples(chapter_id):
    examples = TextbookCompanionExample.objects.using('scilab')\
        .filter(chapter_id=chapter_id).filter(cloud_err_status=0)\
        .order_by('number')
    return examples


def get_revisions(example_id):
    example_file = TextbookCompanionExampleFiles.objects.using('scilab')\
        .get(example_id=example_id, filetype='S')
    commits = utils.get_commits(file_path=example_file.filepath)
    return commits


def get_code(file_path, commit_sha):
    file = utils.get_file(file_path, commit_sha, main_repo=True)
    return file


def index(request):
    context = {}
    book_id = request.GET.get('book_id')
    user = request.user
    # if not user.is_anonymous():
    #     social = user.social_auth.get(provider='google-oauth2')
    #     url = 'https://www.googleapis.com/plus/v1/people/me'
    #     params = {'access_token': social.extra_data['access_token']}
    #     # r = requests.get(url, params=params)
    #     # print(r.content)

    #     context = {
    #         'user': user
    #     }

    if not (request.GET.get('eid') or request.GET.get('book_id')):
        catg_all = catg(None, all_cat=True)
        subcatg_all = subcatg(None, all_subcat=True)
        context = {
            'catg': catg_all,
            'subcatg': subcatg_all,
        }
        if 'maincat_id' in request.session:
            maincat_id = request.session['maincat_id']
            context['maincat_id'] = int(maincat_id)
            context['subcatg'] = get_subcategories(maincat_id)

        if 'subcategory_id' in request.session:
            category_id = request.session['subcategory_id']
            context['subcategory_id'] = int(category_id)
            context['books'] = get_books(category_id)

        if 'book_id' in request.session:
            book_id = request.session['book_id']
            context['book_id'] = int(book_id)
            context['chapters'] = get_chapters(book_id)

        if 'chapter_id' in request.session:
            chapter_id = request.session['chapter_id']
            context['chapter_id'] = int(chapter_id)
            context['examples'] = get_examples(chapter_id)

        if 'example_id' in request.session:
            example_id = request.session['example_id']
            context['eid'] = int(example_id)
            context['revisions'] = get_revisions(example_id)
            review = ScilabCloudComment.objects.using('scilab')\
                .filter(example=example_id).count()
            review_url = "http://scilab.in/cloud_comments/" + str(example_id)
            context['review'] = review
            context['review_url'] = review_url

        if 'commit_sha' in request.session:
            commit_sha = request.session['commit_sha']
            context['commit_sha'] = commit_sha

            if 'code' in request.session:
                session_code = request.session['code']
                context['code'] = session_code
            elif 'filepath' in request.session:
                session_code = get_code(
                    request.session['filepath'], commit_sha)
                context['code'] = session_code
        context['garuda_server'] = GARUDA_SERVER
        template = loader.get_template('index.html')
        return HttpResponse(template.render(context, request))
    elif book_id:
        books = TextbookCompanionPreference.objects\
            .db_manager('scilab').raw("""
                        SELECT DISTINCT (loc.category_id),pe.id,
                        tcbm.sub_category,loc.maincategory, pe.book as
                        book,loc.category_id,tcbm.sub_category,
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
                        pe.cloud_pref_err_status = 0 AND
                        pe.id=%s""", [book_id])
        books = list(books)

        if len(books) == 0:
            catg_all = catg(None, all_cat=True)
            context = {
                'catg': catg_all,
                'err_msg': """This TBC is not supported by Scilab on Cloud."""\
                           """You can download TBC from www.scilab.in. You """\
                           """ are redirected to scilab on cloud home page."""
            }

            template = loader.get_template('index.html')
            context['garuda_server'] = GARUDA_SERVER
            return HttpResponse(template.render(context, request))

        books = get_books(books[0].sub_category)
        maincat_id = books[0].category_id
        subcat_id = books[0].sub_category
        request.session['maincat_id'] = maincat_id
        request.session['subcategory_id'] = subcat_id
        request.session['book_id'] = book_id
        chapters = get_chapters(book_id)
        subcateg_all = TextbookCompanionSubCategoryList.objects\
            .using('scilab').filter(maincategory_id=maincat_id)\
            .order_by('subcategory_id')
        categ_all = TextbookCompanionCategoryList.objects.using('scilab')\
            .filter(~Q(category_id=0)).order_by('maincategory')
        context = {
            'catg': categ_all,
            'subcatg': subcateg_all,
            'maincat_id': maincat_id,
            'chapters': chapters,
            'subcategory_id': books[0].sub_category,
            'books': books,
            'book_id': int(book_id),

        }
        context['garuda_server'] = GARUDA_SERVER
        template = loader.get_template('index.html')
        return HttpResponse(template.render(context, request))
    else:
        try:
            eid = int(request.GET['eid'])
        except ValueError:
            context = {
                'catg': catg_all,
                'err_msg': """This TBC example is not available """\
                           """on Scilab on Cloud. You can download """\
                           """TBC example from www.scilab.in."""
            }
            context['garuda_server'] = GARUDA_SERVER
            return render(request, 'website/templates/index.html', context)

        if eid:
            try:
                review = ScilabCloudComment.objects.using('scilab')\
                    .filter(example=eid).count()
                review_url = "http://scilab.in/cloud_comments/" + str(eid)

                examples = TextbookCompanionExample.objects\
                    .db_manager('scilab').raw("""
                        SELECT id, id as example_id,
                            caption, number, chapter_id
                        FROM textbook_companion_example
                        WHERE cloud_err_status=0 AND
                              chapter_id = (SELECT chapter_id
                                            FROM textbook_companion_example
                                            WHERE id =%s)""", [eid])
                chapter_id = examples[0].chapter_id
                chapters = TextbookCompanionChapter.objects\
                    .db_manager('scilab').raw("""
                        SELECT id, name, number, preference_id
                        FROM textbook_companion_chapter
                        WHERE cloud_chapter_err_status = 0 AND
                        preference_id = (SELECT preference_id
                        FROM textbook_companion_chapter WHERE id = %s)
                        ORDER BY number ASC""", [chapter_id])
                preference_id = chapters[0].preference_id

                books = TextbookCompanionPreference.objects\
                    .db_manager('scilab').raw("""
                        SELECT DISTINCT (loc.category_id),pe.id,
                        tcbm.sub_category,loc.maincategory, pe.book as
                        book,loc.category_id,tcbm.sub_category,
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
                        pe.cloud_pref_err_status = 0 AND
                        pe.id=%s""", [preference_id])

                books = get_books(books[0].sub_category)
                maincat_id = books[0].category_id
                subcat_id = books[0].sub_category
                try:
                    example_file = TextbookCompanionExampleFiles.objects\
                        .using('scilab').get(example_id=eid, filetype='S')
                except TextbookCompanionExampleFiles.DoesNotExist:
                    return redirect('/')
                ex_views_count = TextbookCompanionExampleViews.objects\
                    .db_manager('scilab').raw(dedent("""\
                    SELECT id, views_count FROM\
                    textbook_companion_example_views\
                    WHERE example_id=%s """), [eid])

                request.session['maincat_id'] = maincat_id
                request.session['subcategory_id'] = subcat_id
                request.session['book_id'] = preference_id
                request.session['chapter_id'] = chapter_id
                request.session['example_id'] = eid
                request.session['example_file_id'] = example_file.id
                request.session['filepath'] = example_file.filepath
                revisions = get_revisions(eid)
                context['revisions'] = get_revisions(example_id)
                code = get_code(example_file.filepath, revisions[0]['sha'])
                request.session['commit_sha'] = revisions[0]['sha']

            except IndexError:
                categ_all = TextbookCompanionCategoryList.objects\
                .using('scilab').filter(~Q(category_id=0))\
                .order_by('maincategory')
                context = {
                    'catg': categ_all,
                    'err_msg': """This TBC example is not available """\
                               """on Scilab on Cloud. You can download """\
                               """TBC example from www.scilab.in."""
                }
                template = loader.get_template('index.html')
                return HttpResponse(template.render(context, request))

            subcateg_all = TextbookCompanionSubCategoryList.objects\
                .using('scilab').filter(maincategory_id=maincat_id)\
                .order_by('subcategory_id')
            categ_all = TextbookCompanionCategoryList.objects.using('scilab')\
                .filter(~Q(category_id=0)).order_by('maincategory')
            if len(list(ex_views_count)) == 0:
                ex_views_count = 0
            else:
                ex_views_count = ex_views_count[0].views_count
            context = {
                'catg': categ_all,
                'subcatg': subcateg_all,
                'maincat_id': maincat_id,
                'subcategory_id': books[0].sub_category,
                'books': books,
                'book_id': preference_id,
                'chapters': chapters,
                'chapter_id': chapter_id,
                'examples': examples,
                'eid': eid,
                'revisions': revisions,
                'commit_sha': revisions[0]['sha'],
                'code': code,
                'ex_views_count': ex_views_count,
                'review': review,
                'review_url': review_url,
            }

            if not user.is_anonymous:
                context['user'] = user
            context['garuda_server'] = GARUDA_SERVER
            template = loader.get_template('index.html')
            return HttpResponse(template.render(context, request))


def login(request):
    context = {}
    return render(request, 'website/templates/login.html', context)

# def logout(request):
#     print('logging out..')
#     auth_logout(request)
#     return render_to_response('registration/logged-out.html', {},
#           RequestContext(request))


@user_passes_test(lambda u: u.is_staff)
def review(request):
    revisions = TextbookCompanionRevision.objects.using('scilab') \
        .filter(push_status=0)\
        .order_by('timestamp')

    context = {
        'user': request.user,
        'revisions': revisions,
    }
    return render(request, 'website/templates/review-interface.html', context)


def update_pref_hits(pref_id):
    updatecount = TextbookCompanionPreferenceHits.objects.using('scilab')\
        .filter(pref_id=pref_id)\
        .update(hitcount=F('hitcount') + 1)
    if not updatecount:
        insertcount = TextbookCompanionPreferenceHits.objects.using('scilab')\
            .get_or_create(pref_id=pref_id, hitcount=1)
    return


def search_book(request):
    result = {}
    response_dict = []
    if request.is_ajax():
        exact_search_string = request.GET.get('search_string')
        search_string = "%" + exact_search_string + "%"
        result = TextbookCompanionPreference.objects\
            .db_manager('scilab').raw("""
                            SELECT pe.id, pe.book as book, pe.author as author,
                            pe.publisher as publisher,pe.year as year,
                            pe.id as pe_id, po.approval_date as approval_date
                            FROM textbook_companion_preference pe
                            LEFT JOIN textbook_companion_proposal po ON
                            pe.proposal_id = po.id WHERE
                            (pe.book like %s OR pe.author like %s)
                            AND po.proposal_status = 3
                            AND pe.approval_status = 1
                            ORDER BY (pe.book = %s OR pe.author = %s) DESC,
                            length(pe.book) """,
                                      [search_string, search_string,
                                       str(exact_search_string),
                                       str(exact_search_string)])
        if len(list(result)) == 0:
            response = {
                'book': "Not found",
                'author': "Not found"
            }
            response_dict.append(response)
        else:
            for obj in result:
                update_pref_hits(obj.id)
                response = {
                    'ids': obj.id,
                    'book': obj.book,
                    'author': obj.author,
                }
                response_dict.append(response)
    else:
        response_dict = 'fail'
        response = {'book': "Please try again later!"}
        response_dict.append(response)
    return HttpResponse(simplejson.dumps(response_dict),
                        content_type='application/json')


def popular(request):
    result = {}
    response_dict = []
    if request.is_ajax():
        search_string = request.GET.get('search_string')
        search_string = "%" + search_string + "%"
        result = TextbookCompanionPreference.objects\
            .db_manager('scilab').raw("""
                            SELECT pe.id, pe.book as book, pe.author as author,
                            pe.publisher as publisher,pe.year as year,
                            pe.id as pe_id, po.approval_date as approval_date,
                            tcph.hitcount FROM textbook_companion_preference pe
                            left join textbook_companion_preference_hits tcph on
                            tcph.pref_id = pe.id
                            LEFT JOIN textbook_companion_proposal po ON
                            pe.proposal_id = po.id WHERE po.proposal_status = 3
                            AND pe.approval_status = 1
                            ORDER BY tcph.hitcount DESC LIMIT 10 """)
        if len(list(result)) == 0:
            response = {
                'book': "Not found",
                'author': "Not found"
            }
            response_dict.append(response)
        else:
            for obj in result:
                response = {
                    'ids': int(obj.id),
                    'book': obj.book,
                    'author': obj.author,
                }
                response_dict.append(response)
    else:
        response_dict = 'fail'
        response = {'book': "Please try again later!"}
        response_dict.append(response)
    return HttpResponse(simplejson.dumps(response_dict),
                        content_type='application/json')


def recent(request):
    result = {}
    response_dict = []
    if request.is_ajax():
        exact_search_string = request.GET.get('search_string')
        search_string = "%" + exact_search_string + "%"
        result = TextbookCompanionPreference.objects\
            .db_manager('scilab').raw("""
                            SELECT pe.id, pe.book as book, pe.author as author,
                            pe.publisher as publisher,pe.year as year,
                            pe.id as pe_id, po.approval_date as approval_date,
                            tcph.hitcount, tcph.last_search
                            FROM textbook_companion_preference pe
                            left join textbook_companion_preference_hits tcph
                            on tcph.pref_id = pe.id
                            LEFT JOIN textbook_companion_proposal po ON
                            pe.proposal_id = po.id WHERE po.proposal_status = 3
                            AND pe.approval_status = 1
                            ORDER BY tcph.last_search DESC LIMIT 10 """)
        if len(list(result)) == 0:
            response = {
                'book': "Not found",
                'author': "Not found"
            }
            response_dict.append(response)
        else:
            for obj in result:
                response = {
                    'ids': int(obj.id),
                    'book': obj.book,
                    'author': obj.author,
                }
                response_dict.append(response)
    else:
        response_dict = 'fail'
        response = {'book': "Please try again later!"}
        response_dict.append(response)
    return HttpResponse(simplejson.dumps(response_dict),
                        content_type='application/json')


def update_view_count(request):
    ex_id = request.GET.get('ex_id')
    Example_chapter_id = TextbookCompanionExample.objects.using('scilab')\
        .filter(id=ex_id)

    TextbookCompanionExampleViews.objects.using('scilab')\
        .get_or_create(example_id=ex_id, chapter_id=Example_chapter_id[0]
                       .chapter_id)
    TextbookCompanionExampleViews.objects.using('scilab')\
        .filter(example_id=ex_id)\
        .update(views_count=F('views_count') + 1)

    Example_views_count = TextbookCompanionExampleViews.objects.using('scilab')\
        .filter(example_id=ex_id)
    data = Example_views_count[0].views_count
    return HttpResponse(simplejson.dumps(data),
                        content_type='application/json')

def get_example_detail(eid):
    examples = TextbookCompanionExample.objects\
                    .db_manager('scilab').raw("""
                        SELECT id, id as example_id,
                            caption, number, chapter_id
                        FROM textbook_companion_example
                        WHERE cloud_err_status=0 AND
                              chapter_id = (SELECT chapter_id
                                            FROM textbook_companion_example
                                            WHERE id =%s)""", [eid])
    chapter_id = examples[0].chapter_id
    chapters = TextbookCompanionChapter.objects\
        .db_manager('scilab').raw("""
            SELECT id, name, number, preference_id
            FROM textbook_companion_chapter
            WHERE cloud_chapter_err_status = 0 AND
            preference_id = (SELECT preference_id
            FROM textbook_companion_chapter WHERE id = %s)
            ORDER BY number ASC""", [chapter_id])
    preference_id = chapters[0].preference_id

    books = TextbookCompanionPreference.objects\
        .db_manager('scilab').raw("""
            SELECT DISTINCT (loc.category_id),pe.id,
            los.subcategory,loc.maincategory, pe.book as
            book,loc.category_id,tcbm.sub_category,
            pe.author as author, pe.publisher as publisher,
            pe.year as year, pe.id as pe_id, pe.edition,
            po.approval_date as approval_date
            FROM textbook_companion_preference pe
            LEFT JOIN textbook_companion_proposal po ON
            pe.proposal_id = po.id
            LEFT JOIN textbook_companion_book_main_subcategories
            tcbm ON pe.id = tcbm.pref_id LEFT JOIN list_of_category
            loc ON tcbm.main_category = loc.category_id
            LEFT JOIN list_of_subcategory los ON
            tcbm.sub_category = los.subcategory_id WHERE
            po.proposal_status = 3 AND pe.approval_status = 1
            AND pe.category>0 AND pe.id = tcbm.pref_id AND
            pe.cloud_pref_err_status = 0 AND
            pe.id=%s""", [preference_id])
    details = {
        'book_name' : books[0].book,
        'maincategory_name' : books[0].maincategory,
        'subcategory_name' : books[0].subcategory,
        'author_name' : books[0].author,
        'publisher_name' : books[0].publisher,
        'chapter_number' : chapters[0].number,
        'chapter_name' : chapters[0].name,
        'example_number' : examples[0].number,
        'example_name' : examples[0].caption,
    }
    return (details)
