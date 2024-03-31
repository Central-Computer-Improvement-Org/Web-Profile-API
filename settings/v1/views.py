from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from generic_serializers.serializers import ResponseSerializer, GenericErrorSerializer
from common.exceptions import not_found_exception_handler, bad_request_exception_handler, validation_exception_handler

from .serializers import SettingSerializer, ContactSerializer
from ..models import Setting, Contact

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
            return bad_request_exception_handler(request, "Setting", "Cant create more than 1 settings.")

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
            return not_found_exception_handler(request, 'Setting')
        
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
    
class ContactViewSet(viewsets.ModelViewSet):
    serializer_class = ContactSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        contacts = Contact.objects.all()

        serializer = ResponseSerializer({
            'code': 200,
            'status': 'success',
            'recordsTotal': contacts.count(),
            'data': ContactSerializer(contacts, many=True).data,
            'error': None,
        })

        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        data = request.data
        data['id'] = "CNT-" + datetime.now().strftime('%Y%m%d%H%M%S')

        serializer = self.get_serializer(data=data)

        if not serializer.is_valid():
            return validation_exception_handler(request, serializer.errors)
        
        self.perform_create(serializer)
        
        resp = ResponseSerializer({
            'code': 201,
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
        

