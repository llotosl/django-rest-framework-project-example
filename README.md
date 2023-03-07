This is DRF project example with:
1. JWT Authentication(based on simplejwt).
2. Users Endpoints(based on djoser).
3. News Model with comments and likes(
    used Viewsets,
    GenericAPIViews,
    APIViews,
    annotation for ORM,
)
4. Celery(with /api/v1/news/<id>/send-email/ task).
5. Documentation(based on drf-yasg, url /swagger/ and /redoc/), Django Debug Toolbar and Admin Panel in debug mode.