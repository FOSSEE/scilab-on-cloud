from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'website.views.index', name='index'),

    # Ajax urls
    url(r'^ajax-books/$', 'website.views.ajax_books', name='ajax_books'),
    url(r'^ajax-chapters/$', 'website.views.ajax_chapters', name='ajax_chapters'),
    url(r'^ajax-examples/$', 'website.views.ajax_examples', name='ajax_examples'),
    url(r'^ajax-execute/$', 'website.views.ajax_execute', name='ajax_execute'),
)
