from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.serializers import ListSerializer

from generic_serializers.serializers import ResponseSerializer, GenericErrorSerializer
from auth.auth import IsSuperUser, IsPengurus

from .serializers import UserSerializer
from ..models import User


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
    permission_classes = [IsPengurus]
    authentication_classes = [JWTAuthentication]

    def list(self, request, *args, **kwargs):
        users = User.objects.all()

        serializer = ResponseSerializer({
            'code': 200,
            'status': 'success',
            'recordsTotal': users.count(),
            'data': UserSerializer(users, many=True).data,
            'error': None,
        })

        return Response(serializer.data)
