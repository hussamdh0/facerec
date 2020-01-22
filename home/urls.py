from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^user/$', views.user, name='user'),
    url(r'^lists/$', views.lists, name='lists'),
    url(r'^(?P<user_id>[0-9]+)/$', views.detail, name='detail'),
]
