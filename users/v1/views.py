import django_filters.rest_framework
from django.utils import timezone

from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.serializers import ListSerializer

import common.orderings

from generic_serializers.serializers import ResponseSerializer, GenericErrorSerializer
from auth.auth import IsNotMember
from . import filtersets

from common.orderings import KeywordOrderingFilter
from common.pagination import GenericPaginator

from django.db.models import Q

from .serializers import UserSerializer, DivisionSerializer, RoleSerializer
from ..models import User, Role, Division


class UserProfileViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        profile = User.objects.get(nim=request.user.nim)

        if profile:
            serializer = ResponseSerializer({
                'code': 200,
                'status': 'success',
                'recordsTotal': 1,
                'data': UserSerializer(profile).data,
                'error': None,
            })
        else:
            serializer = ResponseSerializer({
                'code': 404,
                'status': 'NOT FOUND ERROR',
                'recordsTotal': 0,
                'data': None,
                'error': GenericErrorSerializer({
                    'name': 'Not Found',
                    'message': 'Profile not found',
                    'validation': None,
                }).data
            })

        return Response(serializer.data)

class PublicUserViewSet(viewsets.ModelViewSet):
    serializer_class=UserSerializer
    queryset = User.objects.filter(active=True)
    permission_classes = [AllowAny]
    filter_backends = [filtersets.UserSearchFilter, django_filters.rest_framework.DjangoFilterBackend,
                       common.orderings.KeywordOrderingFilter]
    filterset_class = filtersets.UserFilterSet
    ordering_fields = ['createdAt', 'updatedAt']
    ordering = ['created_at']
    pagination_class = common.pagination.GenericPaginator
    authentication_classes = []

    def list(self, request, *args, **kwargs):
        if request.query_params.get('nim'):
            try :
                user = User.objects.get(nim=request.query_params.get('nim'))

                if user.role.name == 'Superadmin':
                    raise NotFound('User not found!')

                serializer = ResponseSerializer({
                    'code': 200,
                    'status': 'success',
                    'recordsTotal': 1,
                    'data': UserSerializer(user).data,
                    'error': None,
                })

                return Response(serializer.data)
            except User.DoesNotExist:
                raise NotFound('User not found!')

        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.exclude(role_id__name='Superadmin')
        
        page = self.paginate_queryset(queryset)

        serializer = ResponseSerializer({
            'code': 200,
            'status': 'success',
            'recordsTotal': queryset.count(),
            'data': UserSerializer(page, many=True).data,
            'error': None,
        })

        return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsNotMember]
    authentication_classes = [JWTAuthentication]
    filter_backends = [filtersets.UserSearchFilter, django_filters.rest_framework.DjangoFilterBackend,
                       common.orderings.KeywordOrderingFilter]
    filterset_class = filtersets.UserFilterSet
    ordering_fields = ['createdAt', 'updatedAt', 'name', 'roleId', 'divisionId']
    ordering = ['created_at']
    pagination_class = common.pagination.GenericPaginator

    def list(self, request, *args, **kwargs):
        if request.query_params.get('nim'):
            user = User.objects.get(nim=request.query_params.get('nim'))

            if user.role_id.name == 'Superadmin':
                raise NotFound('User not found!')

            context = {
                "is_singular": True,
            }

            serializer = ResponseSerializer({
                'code': 200,
                'status': 'success',
                'recordsTotal': 1,
                'data': UserSerializer(user, context=context).data,
                'error': None,
            })

            return Response(serializer.data)

        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.exclude(role_id__name='Superadmin')

        page = self.paginate_queryset(queryset)

        serializer = ResponseSerializer({
            'code': 200,
            'status': 'success',
            'recordsTotal': queryset.count(),
            'data': UserSerializer(page, many=True).data,
            'error': None,
        })

        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        if request.query_params.get('nim') is None:
            raise ValueError('NIM is required')

        user = User.objects.get(nim=request.query_params['nim'])
        serializer = UserSerializer(user, data=request.data, partial=True, context={
            'request': request
        })

        if serializer.is_valid():
            serializer.save()

            response = ResponseSerializer({
                'code': 200,
                'status': 'success',
                'recordsTotal': 1,
                'data': {
                    "message": "Update user success",
                },
                'error': None,
            })

            return Response(response.data)
        else:
            raise ValidationError(serializer.errors)

    def destroy(self, request, *args, **kwargs):
        if request.query_params.get('nim') is None:
            raise ValueError('NIM is required')

        user = User.objects.get(nim=request.query_params['nim'])

        serializer = UserSerializer(user)

        serializer.delete(user)

        serializer = ResponseSerializer({
            'code': 200,
            'status': 'success',
            'recordsTotal': 1,
            'data': {
                "message": "Delete user success",
            },
            'error': None,
        })

        return Response(serializer.data)


class CMSDivisionViewSet(viewsets.ModelViewSet):
    queryset = Division.objects.all()
    serializer_class = DivisionSerializer
    permission_classes = [IsNotMember]
    authentication_classes = [JWTAuthentication]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, common.orderings.KeywordOrderingFilter]
    filterset_class = filtersets.DivisionFilterSet
    ordering_fields = ['name', 'description', 'createdAt', 'updatedAt']
    ordering = ['name']
    pagination_class = common.pagination.GenericPaginator

    def list(self, request, *args, **kwargs):
        if request.query_params.get('id'):
            division = Division.objects.get(id=request.query_params.get('id'))

            serializer = ResponseSerializer({
                'code': 200,
                'status': 'success',
                'recordsTotal': 1,
                'data': DivisionSerializer(division).data,
                'error': None,
            })

            return Response(serializer.data)

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)

        serializer = ResponseSerializer({
            'code': 200,
            'status': 'success',
            'recordsTotal': queryset.count(),
            'data': DivisionSerializer(page, many=True).data,
            'error': None,
        })

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        if request.query_params.get('id') is None:
            raise ValueError('ID is required')

        division = Division.objects.get(id=request.query_params['id'])

        user = User.objects.filter(division_id=division.id)

        if user.exists():
            raise ValidationError({
                "user": ['Division is still used by user!']
            })

        division.delete()

        serializer = ResponseSerializer({
            'code': 200,
            'status': 'success',
            'recordsTotal': 1,
            'data': {
                "message": "Delete division success",
            },
            'error': None,
        })

        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        if request.query_params.get('id') is None:
            raise ValueError('ID is required')

        division = Division.objects.get(id=request.query_params['id'])

        serializer = DivisionSerializer(division, data=request.data, partial=True,
                                        context={'request': request})

        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        serializer.save()

        serializer = ResponseSerializer({
            'code': 200,
            'status': 'success',
            'recordsTotal': 1,
            'data': {
                "message": "Update division success",
            },
            'error': None,
        })

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = DivisionSerializer(data=request.data, context={'request': request})

        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        serializer.save()

        serializer = ResponseSerializer({
            'code': 200,
            'status': 'success',
            'recordsTotal': 1,
            'data': {
                "message": "Create division success",
            },
            'error': None,
        })

        return Response(serializer.data)


class PublicDivisionViewSet(viewsets.ModelViewSet):
    serializer_class = DivisionSerializer
    permission_classes = [AllowAny]
    pagination_class = common.pagination.GenericPaginator
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, common.orderings.KeywordOrderingFilter]
    ordering_fields = ['name', 'description', 'createdAt', 'updatedAt']
    ordering = ['name']
    filterset_class = filtersets.DivisionFilterSet
    authentication_classes = []

    def list(self, request, *args, **kwargs):
        if request.query_params.get('id'):
            division = Division.objects.get(id=request.query_params.get('id'))

            serializer = ResponseSerializer({
                'code': 200,
                'status': 'success',
                'recordsTotal': 1,
                'data': DivisionSerializer(division).data,
                'error': None,
            })

            return Response(serializer.data)

        self.queryset = Division.objects.all()

        serializer = ResponseSerializer({
            'code': 200,
            'status': 'success',
            'recordsTotal': self.queryset.count(),
            'data': DivisionSerializer(self.queryset, many=True).data,
            'error': None,
        })

        return Response(serializer.data)


class CMSRoleViewSet(viewsets.ModelViewSet):
    serializer_class = RoleSerializer
    permission_classes = [IsNotMember]
    authentication_classes = [JWTAuthentication]

    queryset = Role.objects.all()
    filterset_class = filtersets.RoleFilterSet
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, KeywordOrderingFilter]
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['created_at']
    pagination_class = GenericPaginator

    def list(self, request, *args, **kwargs):
        if request.query_params.get('id'):
            role = Role.objects.get(id=request.query_params.get('id'))

            serializer = ResponseSerializer({
                'code': 200,
                'status': 'success',
                'recordsTotal': 1,
                'data': RoleSerializer(role).data,
                'error': None,
            })

            return Response(serializer.data)

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)

        serializer = ResponseSerializer({
            'code': 200,
            'status': 'success',
            'recordsTotal': queryset.count(),
            'data': RoleSerializer(page, many=True).data,
            'error': None,
        })

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        super(CMSRoleViewSet, self).create(request, *args, **kwargs)

        serializer = ResponseSerializer({
            'code': 201,
            'status': 'success',
            'recordsTotal': 1,
            'data': {
                'message': 'Create role success',
            },
            'error': None,
        })

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        id = request.query_params.get('id', None)

        if id is None:
            raise ValueError('ID is required')

        try:
            role = Role.objects.get(id=request.query_params['id'])
            serializers = self.get_serializer(instance=role, data=request.data, partial=True,
                                              context={'request': request})

            if not serializers.is_valid():
                raise ValidationError(serializers.errors)

            serializers.save()

            resp = ResponseSerializer({
                'code': 200,
                'status': 'success',
                'recordsTotal': 1,
                'data': {
                    'message': 'Update role success',
                },
                'error': None,
            })

            return Response(resp.data)

        except Role.DoesNotExist:
            raise NotFound('Project does not exist!')

    def destroy(self, request, *args, **kwargs):
        id = request.query_params.get('id', None)

        if id is None:
            raise ValueError('ID is required')

        try:
            role = Role.objects.get(id=id)

            resp = ResponseSerializer({
                'code': 666,
                'status': 'Mikiro',
                'recordsTotal': 0,
                'data': {
                    'message': 'Superadmin Raiso dibusek cok',
                },
                'error': None,
            })

            if role.name != 'Superadmin':
                self.perform_destroy(role)
                resp = ResponseSerializer({
                    'code': 200,
                    'status': 'success',
                    'recordsTotal': 0,
                    'data': {
                        'message': 'Delete role success',
                    },
                    'error': None,
                })

            return Response(resp.data)

        except Role.DoesNotExist:
            raise NotFound('Role does not exist!')


class PublicRoleViewSet(viewsets.ModelViewSet):
    serializer_class = RoleSerializer
    permission_classes = [AllowAny]

    queryset = Role.objects.all()
    filterset_class = filtersets.RoleFilterSet
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, KeywordOrderingFilter]
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['created_at']
    pagination_class = common.pagination.GenericPaginator
    authentication_classes = []

    def list(self, request, *args, **kwargs):
        if request.query_params.get('id'):
            role = Role.objects.get(id=request.query_params.get('id'))

            serializer = ResponseSerializer({
                'code': 200,
                'status': 'success',
                'recordsTotal': 1,
                'data': RoleSerializer(role).data,
                'error': None,
            })

            return Response(serializer.data)

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)

        serializer = ResponseSerializer({
            'code': 200,
            'status': 'success',
            'recordsTotal': queryset.count(),
            'data': RoleSerializer(page, many=True).data,
            'error': None,
        })

        return Response(serializer.data)
