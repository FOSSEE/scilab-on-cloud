from django.conf.urls import patterns, include, url
from django.contrib.auth import views as auth_views

urlpatterns = patterns('',
    url(r'^$', 'website.views.index', name='index'),
    url('', include('django.contrib.auth.urls', namespace='auth')),
    url(r'^accounts/login/$', 'website.views.login', name='login'),
)
