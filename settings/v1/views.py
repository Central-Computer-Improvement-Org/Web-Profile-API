from django.utils import timezone

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend

from auth.auth import IsPengurus
from common.orderings import KeywordOrderingFilter

from generic_serializers.serializers import ResponseSerializer, GenericErrorSerializer

from .serializers import SettingSerializer, ContactSerializer
from ..models import Setting, Contact


from copy import deepcopy

class CMSSettingViewSet(viewsets.ModelViewSet):
    serializer_class = SettingSerializer
    permission_classes = [IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        setting = Setting.objects.first()

        if not setting:
            raise NotFound('Setting does not exist!')

        data = request.data.copy()

        serializer = self.get_serializer(setting, data=data, partial=True)

        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        self.perform_update(serializer)

        resp = ResponseSerializer({
            'code': 200,
            'status': 'success',
            'recordsTotal': 1,
            'data': SettingSerializer(setting).data,
            'error': None,
        })

        return Response(resp.data)
    
    def retrieve(self, request, *args, **kwargs):
        setting = Setting.objects.first()

        if not setting:
            serializer = ResponseSerializer({
                'code': 200,
                'status': 'success',
                'recordsTotal': 0,
                'data': SettingSerializer(setting).data,
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
    
class PublicSettingViewSet(viewsets.ModelViewSet):
    serializer_class = SettingSerializer
    permission_classes = [AllowAny]

    def retrieve(self, request, *args, **kwargs):
        setting = Setting.objects.first()

        if not setting:
            serializer = ResponseSerializer({
                'code': 200,
                'status': 'success',
                'recordsTotal': 0,
                'data': SettingSerializer(setting).data,
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
    
class CMSContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['platform', 'created_at', 'updated_at']
    filter_backends = [DjangoFilterBackend, KeywordOrderingFilter]
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['created_at']

    def list(self, request, *args, **kwargs):
        if request.query_params.get('id'):
            contact = Contact.objects.get(id=request.query_params.get('id'))

            serializer = ResponseSerializer({
                'code': 200,
                'status': 'success',
                'recordsTotal': 1,
                'data': ContactSerializer(contact).data,
                'error': None,
            })

            return Response(serializer.data)

        queryset = self.filter_queryset(self.get_queryset())

        serializer = ResponseSerializer({
            'code': 200,
            'status': 'success',
            'recordsTotal': queryset.count(),
            'data': ContactSerializer(queryset, many=True).data,
            'error': None,
        })

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
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
    
    def update(self, request, *args, **kwargs):
        id = request.query_params.get('id', None)
        data = deepcopy(request.data)

        if id is None:
            raise ValueError('ID is required')
        
        try:
            contact = Contact.objects.get(id=id)
            data = request.data.copy()
            serializer = self.get_serializer(contact, data=data, partial=True)

            if not serializer.is_valid():
                raise ValidationError(serializer.errors)
            
            self.perform_update(serializer)
                    
            resp = ResponseSerializer({
                'code': 204,
                'status': 'success',
                'recordsTotal': 1,
                'data': ContactSerializer(contact).data,
                'error': None,
            })

            return Response(resp.data)
        
        except Contact.DoesNotExist:
            raise NotFound('Contact does not exist!')
    
    def destroy(self, request, *args, **kwargs):
        id = request.query_params.get('id', None)

        if id is None:
            raise ValueError('ID is required')
        
        try:
            contact = Contact.objects.get(id=id)
            serializer = ContactSerializer(contact)

            serializer.delete_icon_uri(contact)
            self.perform_destroy(contact)

            resp = ResponseSerializer({
                'code': 204,
                'status': 'success',
                'recordsTotal': 0,
                'data': None,
                'error': None,
            })

            return Response(resp.data)
    
        except Contact.DoesNotExist:
            raise NotFound('Contact does not exist!')
    
class PublicContactViewSet(viewsets.ModelViewSet):
    serializer_class = ContactSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        if request.query_params.get('id'):
            contact = Contact.objects.get(id=request.query_params.get('id'))

            serializer = ResponseSerializer({
                'code': 200,
                'status': 'success',
                'recordsTotal': 1,
                'data': ContactSerializer(contact).data,
                'error': None,
            })

            return Response(serializer.data)

        contacts = Contact.objects.all()

        serializer = ResponseSerializer({
            'code': 200,
            'status': 'success',
            'recordsTotal': contacts.count(),
            'data': ContactSerializer(contacts, many=True).data,
            'error': None,
        })

        return Response(serializer.data)