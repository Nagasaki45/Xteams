from django.urls import re_path

from . import views

app_name = 'groups'
urlpatterns = [
    re_path(r'^$', views.group_list, name='list'),
    re_path(r'^create/$', views.GroupCreate.as_view(), name='create'),
    re_path(r'^(?P<pk>\d+)/$', views.GroupDetail.as_view(), name='detail'),
    re_path(r'^(?P<pk>\d+)/team-up/$', views.team_up, name='team-up'),
    re_path(r'^(?P<pk>\d+)/manage/$', views.Manage.as_view(), name='manage'),
    re_path(r'^(?P<pk>\d+)/delete/$', views.Delete.as_view(), name='delete'),

    # AJAX views
    re_path(r'^change-state/$', views.ChangeState.as_view(), name='change_state'),
]
