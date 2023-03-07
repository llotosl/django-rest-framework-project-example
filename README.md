This is DRF project example with:
1. JWT Authentication (based on simplejwt).
2. Users Endpoints (based on djoser).
3. News Model with comments and likes(\n
    used Viewsets,\n
    GenericAPIViews,\n
    APIViews,\n
    annotation for ORM,\n
)
4. Celery (with /api/v1/news/<id>/send-email/ task).
5. Documentation (based on drf-yasg, url /swagger/ and /redoc/), Django Debug Toolbar and Admin Panel in debug mode.
6. Filters for /api/v1/news/ (based on django-filter).
