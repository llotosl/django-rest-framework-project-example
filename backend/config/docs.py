from django.urls import re_path

from rest_framework.permissions import IsAdminUser

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Generating docs.
schema_view = get_schema_view(
    openapi.Info(
        title="Dummy API",
        default_version='v1',
        description="Dummy description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@dummy.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(IsAdminUser,),
)

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger',
            cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc',
            cache_timeout=0), name='schema-redoc'),
]