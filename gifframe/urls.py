from django.conf.urls import include, url
from django.contrib import admin

from .views import HomeView, IdFrameView, UrlFrameView, ResetFrameView

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^a/(?P<gifId>[a-zA-Z0-9]+)/$', IdFrameView.as_view(), name='idFrames'),
    url(r'^a/(?P<gifId>[^\s]+)/$', UrlFrameView.as_view(), name='urlFrames'),
    url(r'^reset/(?P<gifId>[\d]+)/$', ResetFrameView.as_view(), name='resetFrames'),
    url(r'^$', HomeView.as_view(), name='home')
]
