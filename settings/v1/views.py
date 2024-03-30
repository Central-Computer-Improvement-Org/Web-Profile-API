from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from generic_serializers.serializers import ResponseSerializer, GenericErrorSerializer
from common.exceptions import not_found_exception_handler, server_error_exception_handler, validation_exception_handler

from .serializers import SettingSerializer
from ..models import Setting

from datetime import datetime
from copy import deepcopy

class SettingViewSet(viewsets.ModelViewSet):
    serializer_class = SettingSerializer
    permission_classes = [AllowAny]

    def retrieve(self, request, *args, **kwargs):
        setting = Setting.objects.first()

        if not setting:
            serializer = ResponseSerializer({
                'code': 200,
                'status': 'success',
                'recordsTotal': 0,
                'data': [],
                'error': None
            })

            return Response(serializer.data)

        serializer = ResponseSerializer({
            'code': 200,
            'status': 'success',
            'recordsTotal': 1,
            'data': SettingSerializer(setting).data,
            'error': None,
        })

        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        data = request.data
        data['id'] = "STG-" + datetime.now().strftime('%Y%m%d%H%M%S')

        serializer = self.get_serializer(data=data)

        if not serializer.is_valid():
            return validation_exception_handler(request, serializer.errors)
        
        if Setting.objects.count() > 0:
            return Response({
                'code': 400,
                'status': 'BAD_REQUEST_ERROR',
                'recordsTotal': 0,
                'data': None,
                'error': GenericErrorSerializer({
                    'name': 'Bad Request',
                    'message': 'Setting already exists.',
                    'validation': None,
                }).data
            }, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        
        resp = ResponseSerializer({
            'code': 201,
            'status': 'success',
            'recordsTotal': 1,
            'data': serializer.data,
            'error': None,
        })

        return Response(resp.data)
    
    def update(self, request, *args, **kwargs):
        data = deepcopy(request.data)
        setting = Setting.objects.first()

        if not setting:
            return not_found_exception_handler(request, 'Not Found', 'Data not found')
        
        data['id'] = setting.id
        serializer = self.get_serializer(setting, data=data, partial=True)

        if not serializer.is_valid():
            return validation_exception_handler(request, serializer.errors)
        
        self.perform_update(serializer)

        resp = ResponseSerializer({
            'code': 200,
            'status': 'success',
            'recordsTotal': 1,
            'data': serializer.data,
            'error': None,
        })

        return Response(resp.data)

    def get_permissions(self):
        if self.action == 'create' or self.action == 'update':
            return [IsAuthenticated()]
        return super().get_permissions()