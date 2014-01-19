from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView
from django.core.urlresolvers import reverse

from django.contrib import admin
import settings

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'annual_client_report.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT,
    }),
    url(r'^$', RedirectView.as_view(url=reverse('admin:index'))),
)
