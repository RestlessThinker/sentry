"""
sentry.conf.urls
~~~~~~~~~~~~~~~~

These are additional urls used by the Sentry-provided web server

:copyright: (c) 2012 by the Sentry Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

import os

from sentry.web.urls import urlpatterns as web_urlpatterns
try:
    from django.conf.urls import include, patterns, url
except ImportError:
    # django < 1.5 compat
    from django.conf.urls.defaults import include, patterns, url  # NOQA
from django.contrib import admin
from django.views.defaults import page_not_found

admin.autodiscover()
admin_media_dir = os.path.join(os.path.dirname(admin.__file__), 'media')


handler404 = lambda x: page_not_found(x, template_name='sentry/404.html')


def handler500(request):
    """
    500 error handler.

    Templates: `500.html`
    Context: None
    """
    from django.template import Context, loader
    from django.http import HttpResponseServerError

    context = {'request': request}

    t = loader.get_template('sentry/500.html')
    return HttpResponseServerError(t.render(Context(context)))

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^500/', handler500),
    url(r'^404/', handler404),
) + web_urlpatterns
