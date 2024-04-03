from django.utils import timezone
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from auth.auth import IsPengurus
from generic_serializers.serializers import ResponseSerializer
from news.news_models import News
from news.v1.serializers import NewsSerializer


class CMSNewsViewSet(viewsets.ModelViewSet):
    serializer_class = NewsSerializer
    permission_classes = [IsPengurus]

    def create(self, request, *args, **kwargs):
        super(CMSNewsViewSet, self).create(request, *args, **kwargs)

        serializer = ResponseSerializer({
            'code': 200,
            'status': 'success',
            'recordsTotal': 1,
            'data': None,
            'error': None,
        })

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        if request.query_params.get('id') is None:
            raise ValueError('ID is required')

        news = News.objects.get(id=request.query_params['id'])
        news.delete()

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

        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        news = News.objects.get(id=request.query_params['id'])
        news.title = request.data['title']
        news.description = request.data['description']
        news.updated_at = timezone.now()
        news.updated_by = request.user.nim
        news.save()

        serializer = ResponseSerializer({
            'code': 200,
            'status': 'success',
            'recordsTotal': 1,
            'data': NewsSerializer(news).data,
            'error': None,
        })

        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        if request.query_params.get('id'):
            news = News.objects.get(id=request.query_params.get('id'))

            serializer = ResponseSerializer({
                'code': 200,
                'status': 'success',
                'recordsTotal': 1,
                'data': NewsSerializer(news).data,
                'error': None,
            })

            return Response(serializer.data)

        self.queryset = News.objects.all()

        serializer = ResponseSerializer({
            'code': 200,
            'status': 'success',
            'recordsTotal': self.queryset.count(),
            'data': NewsSerializer(self.queryset, many=True).data,
            'error': None,
        })

        return Response(serializer.data)


class PublicNewsViewSet(viewsets.ModelViewSet):
    serializer_class = NewsSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        if request.query_params.get('id'):
            news = News.objects.get(id=request.query_params.get('id'))

            serializer = ResponseSerializer({
                'code': 200,
                'status': 'success',
                'recordsTotal': 1,
                'data': NewsSerializer(news).data,
                'error': None,
            })

            return Response(serializer.data)

        serializer = ResponseSerializer({
            'code': 200,
            'status': 'success',
            'recordsTotal': self.queryset.count(),
            'data': NewsSerializer(self.queryset, many=True).data,
            'error': None,
        })

        return Response(serializer.data)
