from datetime import datetime

from django.db.models import Q
from rest_framework import filters

import django_filters


class EventSearchFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        search_param = request.query_params.get('search', None)
        if search_param:
            queryset = queryset.filter(Q(title__icontains=search_param))
        return queryset


class EventFilterSet(django_filters.FilterSet):
    startDate = django_filters.CharFilter(method='filter_startDate')
    endDate = django_filters.CharFilter(method='filter_endDate')
    isPublished = django_filters.BooleanFilter(field_name='is_published')

    def filter_startDate(self, queryset, name, value):
        try:
            start_date = datetime.strptime(value, "%d-%m-%Y %H:%M")
            return queryset.filter(**{f"startDate__gte": start_date.strftime('%Y-%m-%d %H:%M')})
        except ValueError:
            return queryset.none()

    def filter_endDate(self, queryset, name, value):
        try:
            end_date = datetime.strptime(value, "%d-%m-%Y %H:%M")
            return queryset.filter(**{f"endDate__lte": end_date.strftime('%Y-%m-%d %H:%M')})
        except ValueError:
            return queryset.none()