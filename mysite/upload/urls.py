from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
        url(r'^top$', 'upload.views.demo', name='demo'),
)
