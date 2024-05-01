import django_filters.rest_framework
from django.core.exceptions import BadRequest
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.serializers import ListSerializer

from generic_serializers.serializers import ResponseSerializer, GenericErrorSerializer
from auth.auth import IsSuperUser, IsPengurus
from . import filtersets

from .serializers import UserSerializer, DivisionSerializer
from ..models import User
from ..models_divisions import Division


class UserProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

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


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsPengurus]
    authentication_classes = [JWTAuthentication]
    filter_backends = [filtersets.UserSearchFilter, django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = filtersets.UserFilterSet

    def list(self, request, *args, **kwargs):
        if request.query_params.get('nim'):
            user = User.objects.get(nim=request.query_params.get('nim'))

            serializer = ResponseSerializer({
                'code': 200,
                'status': 'success',
                'recordsTotal': 1,
                'data': UserSerializer(user).data,
                'error': None,
            })

            return Response(serializer.data)

        queryset = self.filter_queryset(self.get_queryset())

        serializer = ResponseSerializer({
            'code': 200,
            'status': 'success',
            'recordsTotal': queryset.count(),
            'data': UserSerializer(queryset, many=True).data,
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
                'data': None,
                'error': None,
            })

            return Response(response.data)
        else:
            raise ValidationError(serializer.errors)


class CMSDivisionViewSet(viewsets.ModelViewSet):
    serializer_class = DivisionSerializer
    permission_classes = [IsPengurus]
    authentication_classes = [JWTAuthentication]

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

        divisions = Division.objects.all()

        serializer = ResponseSerializer({
            'code': 200,
            'status': 'success',
            'recordsTotal': divisions.count(),
            'data': DivisionSerializer(divisions, many=True).data,
            'error': None,
        })

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        if request.query_params.get('id') is None:
            raise ValueError('ID is required')

        division = Division.objects.get(id=request.query_params['id'])
        division.delete()

        serializer = ResponseSerializer({
            'code': 200,
            'status': 'success',
            'recordsTotal': 1,
            'data': None,
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
            'data': None,
            'error': None,
        })

        return Response(serializer.data)


class PublicDivisionViewSet(viewsets.ModelViewSet):
    serializer_class = DivisionSerializer
    permission_classes = [AllowAny]

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
