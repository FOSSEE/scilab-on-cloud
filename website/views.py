from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from django.core.context_processors import csrf
from django.contrib.auth import logout
from website.models import TextbookCompanionCategoryList, ScilabCloudComment,\
    TextbookCompanionSubCategoryList, TextbookCompanionProposal,\
    TextbookCompanionPreference, TextbookCompanionChapter,\
    TextbookCompanionExample, TextbookCompanionExampleFiles,\
    TextbookCompanionRevision, TextbookCompanionExampleDependency,\
    TextbookCompanionDependencyFiles
from soc.config import UPLOADS_PATH
import utils
import base64

def catg(cat_id, all_cat):
    if all_cat is False:
        category = TextbookCompanionCategoryList.objects.using('scilab')\
                    .get(id=cat_id)
        return category.category_name
    else:
        category = TextbookCompanionCategoryList.objects.using('scilab')\
                    .all().order_by('category_name')
        return category


def get_books(category_id):
    ids = TextbookCompanionProposal.objects.using('scilab')\
            .filter(proposal_status=3).values('id')
    books = TextbookCompanionPreference.objects.using('scilab')\
        .filter(category=category_id).filter(approval_status=1)\
        .filter(proposal_id__in=ids).order_by('book')
    return books


def get_chapters(book_id):
    chapters = TextbookCompanionChapter.objects.using('scilab')\
                    .filter(preference_id=book_id).order_by('number')
    return chapters


def get_examples(chapter_id):
    examples = TextbookCompanionExample.objects.using('scilab')\
            .filter(chapter_id=chapter_id).order_by('number')
    return examples


def get_revisions(example_id):
    example_file = TextbookCompanionExampleFiles.objects.using('scilab')\
        .get(example_id=example_id, filetype='S')
    commits = utils.get_commits(file_path=example_file.filepath)
    return commits


def get_code(file_path, commit_sha):
    file = utils.get_file(file_path, commit_sha, main_repo=True)
    code = base64.b64decode(file['content'])
    return code


def index(request):
    context = {}

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

    if not request.GET.get('eid'):
        catg_all = catg(None, all_cat=True)
        context = {
            'catg': catg_all,
        }

        if 'category_id' in request.session:
            category_id = request.session['category_id']
            context['category_id'] = int(category_id)
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
                context['code'] = request.session['code']
            elif 'filepath' in request.session:
                context['code'] = get_code(request.session['filepath'], commit_sha)

        return render(request, 'website/templates/index.html', context)
    else:
        try:
            eid = int(request.GET['eid'])
        except ValueError:
            return redirect("/")

        if eid:
            try:
                review = ScilabCloudComment.objects.using('scilab')\
                         .filter(example=eid).count()
                review_url = "http://scilab.in/cloud_comments/" + str(eid)
                categ_all = TextbookCompanionCategoryList.objects\
                    .using('scilab').all().order_by('category_name')
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
                        SELECT id, name,
                            number, preference_id
                        FROM textbook_companion_chapter
                        WHERE cloud_chapter_err_status = 0 AND
                              preference_id = (SELECT preference_id
                                               FROM textbook_companion_chapter
                                               WHERE id = %s)
                                               ORDER BY number ASC""", [chapter_id])
                preference_id = chapters[0].preference_id

                books = TextbookCompanionPreference.objects\
                    .db_manager('scilab').raw("""
                        SELECT pre.id, pre.book,
                            author, category
                        FROM textbook_companion_preference pre
                        WHERE pre.approval_status=1 AND
                              pre.category = (SELECT category
                                              FROM textbook_companion_preference
                                              WHERE id = %s) AND
                              cloud_pref_err_status=0 AND
                              pre.proposal_id IN (SELECT id
                                                  FROM textbook_companion_proposal 
                                                  WHERE proposal_status=3)
                        ORDER BY pre.book ASC""", [preference_id])
                category_id = books[0].category
                example_file = TextbookCompanionExampleFiles.objects.using('scilab')\
                    .get(example_id=eid, filetype='S')

                request.session['category_id'] = category_id
                request.session['book_id'] = preference_id
                request.session['chapter_id'] = chapter_id
                request.session['example_id'] = eid
                request.session['example_file_id'] = example_file.id
                request.session['filepath'] = example_file.filepath

                revisions = get_revisions(eid)
                code = get_code(example_file.filepath, revisions[0]['sha'])
                request.session['commit_sha'] = revisions[0]['sha']

            except IndexError:
                return redirect("/")

            context = {
                'catg': categ_all,
                'category_id': category_id,
                'books': books,
                'book_id': preference_id,
                'chapters': chapters,
                'chapter_id': chapter_id,
                'examples': examples,
                'eid': eid,
                'revisions': revisions,
                'commit_sha': revisions[0]['sha'],
                'code': code,
                'review': review,
                'review_url': review_url,
            }

            if not user.is_anonymous():
                context['user'] = user

            return render(request, 'website/templates/index.html', context)


def login(request):
    context = {}
    return render(request, 'website/templates/login.html', context)

# def logout(request):
#     print('logging out..')
#     auth_logout(request)
#     return render_to_response('registration/logged-out.html', {}, RequestContext(request))


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
