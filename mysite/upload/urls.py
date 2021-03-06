from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
        # login
        url(r'^$', 'upload.views.login_page', name='login_page'),
        url(r'^login/$', 'upload.views.login_page', name='login_page'),

        # upload
        url(r'^upload/$', 'upload.views.upload', name='upload'),
        url(r'upload/sort_by_file/$', 'upload.views.file_sort', name='file_sort'),
        url(r'upload/download/(?P<id>\d+)/$', 'upload.views.upload_file_op', name='upload_file_op'),
        url(r'upload/delete/(?P<id>\d+)/$', 'upload.views.upload_delete', name='upload_delete'),

        # email validate
        url(r'^upload/(?P<user>\D+)/(?P<key>\w+)/$', \
                'upload.views.validate_email', name='validate_email'),

        # logout
        url(r'^logout/$', 'upload.views.logout_page', name='logout_page'),
)
