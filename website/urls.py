from django.conf.urls import patterns, include, url
# from django.contrib.auth import views as auth_views
from website import views
from website import ajax

urlpatterns = patterns(
    '',
    url(r'^$', 'website.views.landing', name='landing'),
    url(r'^index$', 'website.views.index', name='index'),
    url('', include('django.contrib.auth.urls', namespace='auth')),
    url(r'^submit-revision/$', 'website.ajax.revision_form',
        name='revision_form'),
    url(r'^update_view_count/$', 'website.views.update_view_count',
        name='update_view_count'),
    url(r'^search_book/$', 'website.views.search_book'),
    url(r'^search_book/popular/$', 'website.views.popular'),
    url(r'^search_book/recent/$', 'website.views.recent'),

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
