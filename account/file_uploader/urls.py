from django.conf.urls import patterns, url
from file_uploader.FileUpload import SnapUpload


urlpatterns = patterns('',
    # Examples:
    #Upload File
    #url(r'^$', RegisterView.as_view(), name='uim.register.create.home'),
    url(r'^snap/$', SnapUpload.as_view(), name='uim.file.upload.snap'),
)