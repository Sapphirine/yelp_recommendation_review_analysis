from django.conf.urls import patterns, url
import os

from MinerDemo import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^searchReview/$', views.searchReview, name='searchReview'),
    # url(r'^saveRelation/$', views.saveRelation, name='saveRelation'),
    url(r'^image/(?P<path>.*)','django.views.static.serve',{'document_root':os.path.join(os.path.dirname(__file__)) + '/resource/image/'}),
    url(r'^js/(?P<path>.*)','django.views.static.serve',{'document_root':os.path.join(os.path.dirname(__file__)) + '/resource/js/'}),
    url(r'^css/(?P<path>.*)','django.views.static.serve',{'document_root':os.path.join(os.path.dirname(__file__)) + '/resource/css/'}),  
    url(r'^files/(?P<path>.*)','django.views.static.serve',{'document_root':os.path.join(os.path.dirname(__file__)) + '/resource/files/'}),
)