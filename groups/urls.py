from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^$', views.group_list, name='list'),
    url(r'^create/$', views.GroupCreate.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/$', views.GroupDetail.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/team-up/$', views.team_up, name='team-up'),
    url(r'^(?P<pk>\d+)/manage/$', views.Manage.as_view(), name='manage'),

    # AJAX views
    url(r'^change-state/$', views.ChangeState.as_view(), name='change_state'),
]
