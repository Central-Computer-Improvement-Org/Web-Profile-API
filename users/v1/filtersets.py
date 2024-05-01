from datetime import datetime

from django.db.models import Q
from rest_framework import filters

import django_filters


class UserSearchFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        search_param = request.query_params.get('search', None)
        if search_param:
            queryset = queryset.filter(Q(name__icontains=search_param) | Q(nim_icontains=search_param), Q(email__icontains=search_param))
        return queryset


class UserFilterSet(django_filters.FilterSet):
    yearUniversityEnrolled = django_filters.CharFilter(method='filter_yearUniversityEnrolled')
    yearCommunityEnrolled = django_filters.CharFilter(method='filter_yearCommunityEnrolled')
    isActive = django_filters.BooleanFilter(field_name='is_active')
    role = django_filters.CharFilter(field_name='role_id', lookup_expr='exact')
    division = django_filters.CharFilter(field_name='division_id', lookup_expr='exact')

    def filter_yearUniversityEnrolled(self, queryset, name, value):
        start_date = datetime.strptime(value, "%d-%m-%Y")

        return queryset.filter(**{f"year_university_enrolled": start_date.strftime('%Y-%m-%d')})

    def filter_yearCommunityEnrolled(self, queryset, name, value):
        start_date = datetime.strptime(value, "%d-%m-%Y")

        return queryset.filter(**{f"year_community_enrolled": start_date.strftime('%Y-%m-%d')})