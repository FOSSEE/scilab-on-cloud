from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'website.views.index', name='index'),
)
