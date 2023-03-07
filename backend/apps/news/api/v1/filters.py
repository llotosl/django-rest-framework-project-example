from django_filters import rest_framework as filters

from apps.news.models import News


class NewsFilterSet(filters.FilterSet):
    ordering = filters.OrderingFilter(
        fields=('id',),
    )

    class Meta:
        model = News
        fields = {
            'title': ('icontains',)
        }
