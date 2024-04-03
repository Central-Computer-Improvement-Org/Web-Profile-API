from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import MethodNotAllowed, ValidationError, NotFound
from rest_framework.permissions import IsAuthenticated, AllowAny

from generic_serializers.serializers import ResponseSerializer, GenericErrorSerializer
from common.exceptions import not_found_exception_handler, validation_exception_handler
from common.utils import id_generator

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
        data['id'] = id_generator("STG")

        serializer = self.get_serializer(data=data)

        if not serializer.is_valid():
            raise ValidationError(serializer.errors)
        
        if Setting.objects.count() > 0:        
            raise MethodNotAllowed('Cant create more than one setting.')

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
            raise NotFound('Setting does not exist!')
        
        data['id'] = setting.id
        serializer = self.get_serializer(setting, data=data, partial=True)

        if not serializer.is_valid():
            raise ValidationError(serializer.errors)
        
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
        
        data['id'] = id_generator("CNT")

        serializer = self.get_serializer(data=data)

        if not serializer.is_valid():
            raise ValidationError(serializer.errors)
        
        self.perform_create(serializer)
        
        resp = ResponseSerializer({
            'code': 201,
            'status': 'success',
            'recordsTotal': 1,
            'data': serializer.data,
            'error': None,
        })

        return Response(resp.data)
    
    def delete(self, request, *args, **kwargs):
        id = request.query_params.get('id', None)

        if id is None:
            raise ValidationError({
                'id': ['No id provided']
            })
        
        try:
            contact = Contact.objects.get(id=id).delete()
            resp = ResponseSerializer({
                'code': 204,
                'status': 'success',
                'recordsTotal': 0,
                'data': SettingSerializer(contact).data,
                'error': None,
            })

            return Response(resp.data)
        
        except Contact.DoesNotExist:
            raise NotFound('Contact does not exist!')
    
    def get_permissions(self):
        if self.action == 'create' or self.action == 'destroy' or self.action == 'update':
            return [IsAuthenticated()]
        return super().get_permissions()
        

