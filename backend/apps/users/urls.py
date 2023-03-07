from django.urls import (
    include,
    path,
)

urlpatterns = [
    path('api/v1/', include('apps.users.api.v1.urls')),
]
