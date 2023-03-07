from django.urls import (
    include,
    path,
)
from django.contrib import admin
from django.conf import settings

from .docs import urlpatterns as docs_urls


urlpatterns = [
    # Admin Panel
    path('admin/', admin.site.urls),
    
    path('', include('apps.core.urls')),
    path('', include('apps.users.urls')),
    path('', include('apps.news.urls')),
]

if settings.DEBUG:
    # Django debug toolbar
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]
    # Docs urls
    urlpatterns += docs_urls
