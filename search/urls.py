from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^result/(?P<keyword>[\w-]+)/$', views.search, name='search'),
    url(r'^collect/$', views.collect, name='collect'),
    url(r'^echo/$', views.echo, name='echo'),
]