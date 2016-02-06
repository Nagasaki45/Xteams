from django.conf.urls import include, url
from django.conf import settings
from django.views.generic.base import TemplateView
from django.contrib.auth.views import login, logout

from django.contrib import admin
admin.autodiscover()

import groups.urls
import core.views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    # accounts
    url(r'^accounts/login/$', login, name='login'),
    url(r'^accounts/logout/$', logout, {'next_page': settings.LOGIN_REDIRECT_URL}, name='logout'),
    url(r'^accounts/register/$', core.views.Register.as_view(), name='register'),

    # contact
    url(r'^contact/$', core.views.Contact.as_view(), name='contact'),

    # about
    url(r'^about/$',
        core.views.TemplateView.as_view(template_name='about.html'),
        name='about'),

    url(r'^', include(groups.urls.urlpatterns, namespace='groups')),
]
