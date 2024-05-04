from datetime import datetime
from rest_framework import filters

import django_filters

from ..models import Award

class AwardSearchFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        search_param = request.query_params.get('search', None)
        if search_param:
            queryset = queryset.filter(title__icontains=search_param)
        return queryset

class AwardFilter(django_filters.FilterSet):
    dateField = django_filters.CharFilter(method='filter_dateField')
    startDate = django_filters.CharFilter(method='filter_startDate')
    endDate = django_filters.CharFilter(method='filter_endDate')
    issuer = django_filters.CharFilter(field_name='issuer', lookup_expr='icontains')
    title = django_filters.NumberFilter(field_name='title')

    dateField_value = "created_at"

    def filter_dateField(self, queryset, name, value):
        if value == 'updatedAt':
            self.dateField_value = "updated_at"
        else:
            self.dateField_value = "created_at"

        return queryset

    def filter_startDate(self, queryset, name, value):
        try:
            start_date = datetime.strptime(value, "%d-%m-%Y %H:%M")
            return queryset.filter(**{f"{self.dateField_value}__gte": start_date.strftime('%Y-%m-%d %H:%M')})
        except ValueError:
            return queryset.none()

    def filter_endDate(self, queryset, name, value):
        try:
            end_date = datetime.strptime(value, "%d-%m-%Y %H:%M")
            return queryset.filter(**{f"{self.dateField_value}__lte": end_date.strftime('%Y-%m-%d %H:%M')})
        except ValueError:
            return queryset.none()

    class Meta:
        model = Award
        fields = []
