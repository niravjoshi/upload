from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
        url(r'^demo$', 'upload.views.demo', name='demo'),
        url(r'^login$', 'upload.views.login', name='login'),
        url(r'^signup$', 'upload.views.signup', name='singup'),
)
