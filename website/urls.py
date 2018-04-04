from django.conf.urls import patterns, include, url
# from django.contrib.auth import views as auth_views
from website import views
from website import ajax

urlpatterns = patterns(
    '',
    #url(r'^$', 'website.views.landing', name='landing'),
    url(r'^$', 'website.views.index', name='index'),
    url(r'^index$', 'website.views.index', name='index'),
    url('', include('django.contrib.auth.urls', namespace='auth')),
    url(r'^submit-revision/$', 'website.ajax.revision_form',
        name='revision_form'),
    url(r'^update_view_count/$', 'website.views.update_view_count',
        name='update_view_count'),
    url(r'^search_book$', 'website.views.search_book', name='search_book'),
    url(r'^search_book/popular/$', 'website.views.popular', name='popular'),
    url(r'^search_book/recent/$', 'website.views.recent', name='recent'),
    url(r'^get_subcategories/$', 'website.ajax.subcategories',
        name='subcategories'),
    url(r'^get_books/$', 'website.ajax.books', name='books'),
    url(r'^get_chapters/$', 'website.ajax.chapters', name='chapters'),
    url(r'^get_examples/$', 'website.ajax.examples', name='examples'),
    url(r'^get_revisions/$', 'website.ajax.revisions', name='revisions'),
    url(r'^get_code/$', 'website.ajax.code', name='code'),
    url(r'^get_diff/$', 'website.ajax.diff', name='diff'),
    url(r'^get_contributor/$', 'website.ajax.contributor', name='contributor'),
    url(r'^get_bug_form/$', 'website.ajax.bug_form', name='bug_form'),
    url(r'^get_bug_form_submit/$',
        'website.ajax.bug_form_submit', name='bug_form_submit'),
    url(r'^get_node/$', 'website.ajax.node', name='node'),
    url(r'^get_submit_revision_form/$',
        'website.ajax.revision_form', name='revision_form'),
    url(r'^get_submit_revision_form_submit/$',
        'website.ajax.revision_form_submit', name='revision_form_submit'),
    url(r'^review/get_review_revision/$',
        'website.ajax.review_revision', name='review_revision'),
    url(r'^review/get_push_revision/$',
        'website.ajax.push_revision', name='push_revision'),
    url(r'^review/get_remove_revision/$',
        'website.ajax.remove_revision', name='remove_revision'),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),

    # google auth
    url('', include('social.apps.django_app.urls', namespace='social')),

    # for review interface
    url(r'^review/$', 'website.views.review', name='review'),

    url(r'^reviewer-login/$', 'django.contrib.auth.views.login',\
        {'template_name': 'admin/login.html'}),
    #url(r'^logout/$', 'website.views.logout', name='logout'),
)
