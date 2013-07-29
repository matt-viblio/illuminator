from django.conf.urls import patterns, url
from django.conf import settings

from viz import views

urlpatterns = patterns( '',
                        url( r'^illuminator/(?P<script_id>[\d]+)/illuminator\.js$', views.illuminator, name='illuminator' ),
                        url( r'^script_data/(?P<script_id>[\d]+)/(?P<data_structure>[\w]+)/$', views.script_data, name='script_data' ),
                        url( r'^vizualize/script/(?P<script_id>[\d]+)/', views.vizualize, name='vizualize' ),
                        url( r'^load_script', views.load_script, name='load_script' ),
                        url( r'^upload_script/', views.upload_script, name='upload_script' ),
                        url( r'', views.default, name='default' ),
#                        url( r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
                        )
