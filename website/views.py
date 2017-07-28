from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from django.core.context_processors import csrf
from website.models import TextbookCompanionCategoryList, ScilabCloudComment,\
    TextbookCompanionSubCategoryList, TextbookCompanionProposal,\
    TextbookCompanionPreference, TextbookCompanionChapter,\
    TextbookCompanionExample, TextbookCompanionExampleFiles,\
    TextbookCompanionRevision, TextbookCompanionExampleDependency,\
    TextbookCompanionDependencyFiles
from soc.config import UPLOADS_PATH


def catg(cat_id, all_cat):
    if all_cat is False:
        category = TextbookCompanionCategoryList.objects.using('scilab')\
                    .get(id=cat_id)
        return category.category_name
    else:
        category = TextbookCompanionCategoryList.objects.using('scilab')\
                    .all().order_by('category_name')
        return category


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
        all_cat = True
        cat_id = 'NULL'
        catg_all = catg(cat_id, all_cat)
        context = {'catg': catg_all}
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
                            .db_manager('scilab').raw(
                            """SELECT id, id as example_id, caption, number,
                            chapter_id FROM textbook_companion_example WHERE
                            cloud_err_status=0 AND chapter_id =
                            (SELECT chapter_id FROM textbook_companion_example
                            WHERE id =%s)""", [eid])
                chapter_id = examples[0].chapter_id
                chapters = TextbookCompanionChapter.objects\
                            .db_manager('scilab').raw("""SELECT id, name,
                            number, preference_id FROM
                            textbook_companion_chapter WHERE
                            cloud_chapter_err_status = 0 AND preference_id = (
                            SELECT preference_id FROM textbook_companion_chapter
                            WHERE id = %s) ORDER BY number ASC""", [chapter_id])
                preference_id = chapters[0].preference_id

                books = TextbookCompanionPreference.objects\
                         .db_manager('scilab').raw("""SELECT pre.id, pre.book,
                         author, category FROM textbook_companion_preference pre
                         WHERE pre.approval_status=1 AND pre.category = (
                         SELECT category FROM textbook_companion_preference
                         WHERE id = %s) AND cloud_pref_err_status=0 and
                         pre.proposal_id IN (SELECT id from
                         textbook_companion_proposal where proposal_status=3
                         ) ORDER BY pre.book ASC""", [preference_id])
                category_id = books[0].category
                example = TextbookCompanionExampleFiles.objects.using('scilab')\
                           .get(example_id=eid, filetype='S')
                example_path = UPLOADS_PATH + '/' + example.filepath
                f = open(example_path)
                code = f.read()
                f.close()

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