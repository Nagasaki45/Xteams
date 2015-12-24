from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^$', views.team_list, name='list'),
    url(r'^create/$', views.TeamCreate.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/$', views.team_detail, name='detail'),
    url(r'^(?P<pk>\d+)/groups/$', views.groups, name='groups'),
    url(r'^(?P<pk>\d+)/manage/$', views.Manage.as_view(), name='manage'),

    # AJAX views
    url(r'^change-state/$', views.ChangeState.as_view(), name='change_state'),
]
