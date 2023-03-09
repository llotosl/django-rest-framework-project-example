from django.urls import (
    include,
    path,
)
from django.contrib import admin
from django.conf import settings

from .docs import urlpatterns as docs_urls


urlpatterns = [
    path('', include('apps.core.urls')),
    path('', include('apps.users.urls')),
    path('', include('apps.news.urls')),
]

# Docs urls
urlpatterns += docs_urls

if settings.DEBUG:
    urlpatterns += [
        # Admin Panel
        path('admin/', admin.site.urls),
        # Django debug toolbar
        path('__debug__/', include('debug_toolbar.urls')),
    ]
