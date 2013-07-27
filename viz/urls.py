from django.conf.urls import patterns, url
from django.conf import settings

from viz import views

urlpatterns = patterns( '',
                        url( r'^illuminator\.js$', views.illuminator, name='illuminator' ),
                        url( r'script_data/(?P<field>[\w]+)/$', views.script_data, name='script_data' ),
                        url( r'', views.home, name='home' ),
#                        url( r'^gallery\.js$', views.gallery, name='gallery' ),
#                       url( r'^flickr/(?P<user>[\w]+)/gallery\.js$', views.user_gallery, name='user' ),
#                        url( r'^flickr/(?P<user>[\w]+)/$', views.user_display, name='user' ),
#                        url( r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
#                        url( r'^$', views.display, name='display' ),
                        )
