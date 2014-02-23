from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
        url(r'^login$', 'upload.views.login_page', name='login_page'),
        url(r'^demo/(?P<id>\d+)/$', 'upload.views.demo', name='demo'),
)
