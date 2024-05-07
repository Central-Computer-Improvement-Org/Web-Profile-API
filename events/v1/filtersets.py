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
    dateField = django_filters.CharFilter(method='filter_dateField')
    startDate = django_filters.CharFilter(method='filter_startDate')
    endDate = django_filters.CharFilter(method='filter_endDate')
    heldOn = django_filters.CharFilter(field_name='held_on')
    isActive = django_filters.BooleanFilter(field_name='is_active')

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