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
    isActive = django_filters.BooleanFilter(field_name='active')
    role = django_filters.CharFilter(field_name='role_id', lookup_expr='exact')
    division = django_filters.CharFilter(field_name='division_id', lookup_expr='exact')
    roleName = django_filters.CharFilter(field_name='role_id__name', lookup_expr='icontains')
    divisionName = django_filters.CharFilter(field_name='division_id__name', lookup_expr='icontains')
    roleNameExact = django_filters.CharFilter(field_name='role_id__name', lookup_expr='exact')
    divisionNameExact = django_filters.CharFilter(field_name='division_id__name', lookup_expr='exact')

    def filter_yearUniversityEnrolled(self, queryset, name, value):
        start_date = datetime.strptime(value, "%d-%m-%Y")

        return queryset.filter(**{f"year_university_enrolled": start_date.strftime('%Y-%m-%d')})

    def filter_yearCommunityEnrolled(self, queryset, name, value):
        start_date = datetime.strptime(value, "%d-%m-%Y")

        return queryset.filter(**{f"year_community_enrolled": start_date.strftime('%Y-%m-%d')})
    
class RoleFilterSet(django_filters.FilterSet):
    dateField = django_filters.CharFilter(method='filter_dateField')
    startDate = django_filters.CharFilter(method='filter_startDate')
    endDate = django_filters.CharFilter(method='filter_endDate')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

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

class DivisionFilterSet(django_filters.FilterSet):
    dateField = django_filters.CharFilter(method='filter_dateField')
    startDate = django_filters.CharFilter(method='filter_startDate')
    endDate = django_filters.CharFilter(method='filter_endDate')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

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