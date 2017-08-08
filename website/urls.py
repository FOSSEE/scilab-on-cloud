from django.conf.urls import patterns, include, url
# from django.contrib.auth import views as auth_views
from website import views

urlpatterns = patterns(
    '',
    url(r'^$', 'website.views.index', name='index'),
    url(r'^index$', 'website.views.index', name='index'),
    url('', include('django.contrib.auth.urls', namespace='auth')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),

    # google auth
    url('', include('social.apps.django_app.urls', namespace='social')),

    # for review interface
    url(r'^review/$', 'website.views.review', name='review'),

    # url(r'^login/$', 'website.views.login', name='login'),
    #url(r'^logout/$', 'website.views.logout', name='logout'),
)
