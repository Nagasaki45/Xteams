from django.conf.urls import patterns, include, url
from django.conf import settings
from django.views.generic.base import TemplateView

from django.contrib import admin
admin.autodiscover()

import teams.urls
import core.views

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    # accounts
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^accounts/logout/$',
        'django.contrib.auth.views.logout',
        {'next_page': settings.LOGIN_REDIRECT_URL},
        name='logout'),
    url(r'^accounts/register/$',
        core.views.Register.as_view(),
        name='register'),

    # contact
    url(r'^contact/$', core.views.Contact.as_view(), name='contact'),

    # about
    url(r'^about/$',
        core.views.TemplateView.as_view(template_name='about.html'),
        name='about'),

    url(r'^', include(teams.urls.urlpatterns, namespace='teams')),
)
