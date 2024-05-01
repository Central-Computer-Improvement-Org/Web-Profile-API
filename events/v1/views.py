import django_filters
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response

from auth.auth import IsPengurus
from events.models import Event
from events.v1 import filtersets
from events.v1.serializers import EventSerializer
from generic_serializers.serializers import ResponseSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsPengurus]
    filter_backends = [filtersets.EventSearchFilter, django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = filtersets.EventFilterSet

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

        serializer = ResponseSerializer({
            'code': 200,
            'status': 'success',
            'recordsTotal': events.count(),
            'data': EventSerializer(events, many=True).data,
            'error': None,
        })

        return Response(serializer.data)
