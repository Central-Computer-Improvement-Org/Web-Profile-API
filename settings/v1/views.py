from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.permissions import AllowAny

from settings.v1.filtersets import ContactFilter, ContactSearchFilter

from auth.auth import IsNotMember
from common.orderings import KeywordOrderingFilter
from common.pagination import GenericPaginator

from generic_serializers.serializers import ResponseSerializer

from .serializers import SettingSerializer, ContactSerializer
from ..models import Setting, Contact


from copy import deepcopy

class CMSSettingViewSet(viewsets.ModelViewSet):
    serializer_class = SettingSerializer
    permission_classes = [IsNotMember]
    
    def update(self, request, *args, **kwargs):
        setting = Setting.objects.first()

        if not setting:
            raise NotFound('Setting does not exist!')

        serializer = self.get_serializer(instance=setting, data=request.data, partial=True, context={'request': request})

        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        serializer.save()

        resp = ResponseSerializer({
            'code': 200,
            'status': 'success',
            'recordsTotal': 1,
            'data': {
                "message": "Update settings success"
            },
            'error': None,
        })

        return Response(resp.data, status=status.HTTP_204_NO_CONTENT)
    
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
    authentication_classes = []

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
    permission_classes = [IsNotMember]
    filterset_class = ContactFilter
    filter_backends = [DjangoFilterBackend, KeywordOrderingFilter, ContactSearchFilter]
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['created_at']
    pagination_class = GenericPaginator

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

        page = self.paginate_queryset(queryset)

        serializer = ResponseSerializer({
            'code': 200,
            'status': 'success',
            'recordsTotal': queryset.count(),
            'data': ContactSerializer(page, many=True).data,
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
            'data': {
                'message': 'Create contact success'
            },
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
                'data': {
                    'message': 'Update contact success'
                },
                'error': None,
            })

            return Response(resp.data, status=status.HTTP_204_NO_CONTENT)
        
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
                'data': {
                    'message': 'Delete contact success'
                },
                'error': None,
            })

            return Response(resp.data, status=status.HTTP_204_NO_CONTENT)
    
        except Contact.DoesNotExist:
            raise NotFound('Contact does not exist!')
    
class PublicContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [AllowAny]
    filterset_class = ContactFilter
    filter_backends = [DjangoFilterBackend, KeywordOrderingFilter, ContactSearchFilter]
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['created_at']
    pagination_class = GenericPaginator
    authentication_classes = []

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

        page = self.paginate_queryset(queryset)

        serializer = ResponseSerializer({
            'code': 200,
            'status': 'success',
            'recordsTotal': queryset.count(),
            'data': ContactSerializer(page, many=True).data,
            'error': None,
        })

        return Response(serializer.data)