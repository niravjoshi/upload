from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
        # login
        url(r'^$', 'upload.views.login_page', name='login_page'),
        url(r'^login/$', 'upload.views.login_page', name='login_page'),

        # upload
        url(r'^upload/$', 'upload.views.upload', name='upload'),
        url(r'upload/(?P<id>\d+)/$', 'upload.views.upload_file_op', name='upload_file_op'),
        url(r'upload/delete/(?P<id>\d+)/$', 'upload.views.upload_delete', name='upload_delete'),

        # logout
        url(r'^logout/$', 'upload.views.logout_page', name='logout_page'),
)
