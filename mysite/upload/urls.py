from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
        url(r'^login/$', 'upload.views.login_page', name='login_page'),
        url(r'^upload/$', 'upload.views.upload', name='upload'),
        url(r'logout/$', 'upload.views.logout_page', name='logout_page'),
)
