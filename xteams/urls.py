from django.conf.urls import include, url
from django.conf import settings
from django.views.generic.base import TemplateView
from django.contrib.auth.views import login, logout

from django.contrib import admin
admin.autodiscover()

import groups.urls
import core.views

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # core
    url(r'^accounts/register/$', core.views.Register.as_view(), name='register'),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^contact/$', core.views.Contact.as_view(), name='contact'),
    url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),

    # groups
    url(r'^', include(groups.urls.urlpatterns, app_name='groups', namespace='groups')),
]
