from django.conf.urls import patterns, include, url
# from django.contrib.auth import views as auth_views

urlpatterns = patterns(
    '',
    url(r'^$', 'website.views.index', name='index'),
    url(r'^index$', 'website.views.index', name='index'),
    url('', include('django.contrib.auth.urls', namespace='auth')),

    # for review interface
    url(r'^review/$', 'website.views.review', name='review'),

    # url(r'^login/$', 'website.views.login', name='login'),
)
