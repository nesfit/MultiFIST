import datetime

import django_filters

from . import models


class WebArchiveSearchFilter(django_filters.FilterSet):
    web_page__url = django_filters.CharFilter(lookup_expr='icontains', label="URL")
    scraped_data = django_filters.CharFilter(lookup_expr='icontains', label="Data")
    accessed_time__gte = django_filters.DateTimeFilter(method='date_time_gte', label="From")
    accessed_time__lte = django_filters.DateTimeFilter(method='date_time_lte', label="To")

    class Meta:
        model = models.WebArchive
        fields = ['web_page', 'scraped_data', 'accessed_time']

    def date_time_gte(self, queryset, name, value):
        return queryset.filter(accessed_time__gte=value)

    def date_time_lte(self, queryset, name, value):
        return queryset.filter(accessed_time__lte=value)
