from django.urls import path

from . import views
from . import ajax

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path(r'submit-revision/', ajax.revision_form,
        name='revision_form'),
path('update_view_count/', views.update_view_count,
        name='update_view_count'),
    path('search_book/', views.search_book, name='search_book'),
    path('search_book/popular/', views.popular, name='popular'),
    path('search_book/recent/', views.recent, name='recent'),
    path('get_subcategories/', ajax.subcategories,
        name='subcategories'),
    path('get_books/', ajax.books, name='books'),
    path('get_chapters/', ajax.chapters, name='chapters'),
    path('get_examples/', ajax.examples, name='examples'),
    path('get_xcos_example/', ajax.xcos_examples, name='xcos_examples'),
    path('get_revisions/', ajax.revisions, name='revisions'),
    path('get_code/', ajax.code, name='code'),
    path('get_diff/', ajax.diff, name='diff'),
    path('get_contributor/', ajax.contributor, name='contributor'),
    path('get_bug_form/', ajax.bug_form, name='bug_form'),
    path('get_bug_form_submit/',
        ajax.bug_form_submit, name='bug_form_submit'),
    path('get_node/', ajax.node, name='node'),
    path('get_submit_revision_form/',
        ajax.revision_form, name='revision_form'),
    path('get_submit_revision_form_submit/',
        ajax.revision_form_submit, name='revision_form_submit'),
    path('review/get_review_revision/',
        ajax.review_revision, name='review_revision'),
    path('review/get_push_revision/',
        ajax.push_revision, name='push_revision'),
    path('review/get_remove_revision/',
        ajax.remove_revision, name='remove_revision'),
    #path('', include('social.apps.django_app.urls', namespace='social')),

    # for review interface
    path('review/', views.review, name='review'),
]
