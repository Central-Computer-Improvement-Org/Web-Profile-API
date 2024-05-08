import django_filters
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

import common.orderings
import common.pagination

from auth.auth import IsNotMember
from events.models import Event
from events.v1 import filtersets
from events.v1.serializers import EventSerializer
from generic_serializers.serializers import ResponseSerializer


class CMSEventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsNotMember]
    filter_backends = [filtersets.EventSearchFilter, django_filters.rest_framework.DjangoFilterBackend, common.orderings.KeywordOrderingFilter]
    filterset_class = filtersets.EventFilterSet
    ordering_fields = ['id', 'name', 'createdAt', 'updatedAt', 'isActive']
    pagination_class = common.pagination.GenericPaginator

    def create(self, request, *args, **kwargs):
        super(CMSEventViewSet, self).create(request, *args, **kwargs)

        serializer = ResponseSerializer({
            'code': 200,
            'status': 'success',
            'recordsTotal': 1,
            'data': {
                "message": "Created event successfully"
            },
            'error': None,
        })

        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        if request.query_params.get('id'):
            event = Event.objects.get(id=request.query_params.get('id'))

            serializer = ResponseSerializer({
                'code': 200,
                'status': 'success',
                'recordsTotal': 1,
                'data': EventSerializer(event).data,
                'error': None,
            })

            return Response(serializer.data)

        events = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(events)

        serializer = ResponseSerializer({
            'code': 200,
            'status': 'success',
            'recordsTotal': events.count(),
            'data': EventSerializer(page, many=True).data,
            'error': None,
        })

        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        if request.query_params.get('id') is None:
            raise ValidationError('ID is required')

        division = Event.objects.get(id=request.query_params['id'])

        serializer = EventSerializer(division, data=request.data, partial=True,
                                     context={'request': request})

        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        serializer.save()

        serializer = ResponseSerializer({
            'code': 200,
            'status': 'success',
            'recordsTotal': 1,
            'data': {
                "message": "Updated event successfully"
            },
            'error': None,
        })

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        if request.query_params.get('id') is None:
            raise ValueError('ID is required')

        event = Event.objects.get(id=request.query_params['id'])

        serializer = EventSerializer(event)
        serializer.delete(event)

        serializer = ResponseSerializer({
            'code': 200,
            'status': 'success',
            'recordsTotal': 1,
            'data': {
                "message": "Deleted event successfully"
            },
            'error': None,
        })

        return Response(serializer.data)


class PublicEventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.filter(is_active=True)
    serializer_class = EventSerializer
    permission_classes = [AllowAny]
    filter_backends = [filtersets.EventSearchFilter, django_filters.rest_framework.DjangoFilterBackend, common.orderings.KeywordOrderingFilter]
    filterset_class = filtersets.EventFilterSet
    ordering_fields = ['id', 'name', 'createdAt', 'updatedAt']
    pagination_class = common.pagination.GenericPaginator

    def list(self, request, *args, **kwargs):
        if request.query_params.get('id'):
            event = Event.objects.get(id=request.query_params.get('id'))

            serializer = ResponseSerializer({
                'code': 200,
                'status': 'success',
                'recordsTotal': 1,
                'data': EventSerializer(event).data,
                'error': None,
            })

            return Response(serializer.data)

        events = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(events)

        serializer = ResponseSerializer({
            'code': 200,
            'status': 'success',
            'recordsTotal': events.count(),
            'data': EventSerializer(page, many=True).data,
            'error': None,
        })

        return Response(serializer.data)

