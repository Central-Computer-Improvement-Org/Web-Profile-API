from datetime import datetime

from django.utils import timezone
from django_filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from auth.auth import IsPengurus
from common.orderings import KeywordOrderingFilter
from common.utils import rename_image_file
from generic_serializers.serializers import ResponseSerializer
from news.detail_news_media import DetailNewsMedia
from news.news_models import News
from news.v1.filtersets import NewsFilter, NewsMediaFilter
from news.v1.serializers import NewsSerializer, DetailNewsMediaSerializer


class CMSNewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsPengurus]
    filter_backends = [DjangoFilterBackend, KeywordOrderingFilter]
    filterset_class = NewsFilter
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['created_at']

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

        news = News.objects.get(id=request.query_params['id'])
        serializer = self.get_serializer(instance=news, data=request.data, partial=True,
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

        queryset = self.filter_queryset(self.get_queryset())

        serializer = ResponseSerializer({
            'code': 200,
            'status': 'success',
            'recordsTotal': queryset.count(),
            'data': NewsSerializer(queryset, many=True).data,
            'error': None,
        })

        return Response(serializer.data)


class PublicNewsViewSet(viewsets.ModelViewSet):
    serializer_class = NewsSerializer
    permission_classes = [AllowAny]
    queryset = News.objects.filter(is_published=True)
    filter_backends = [DjangoFilterBackend, KeywordOrderingFilter]
    filterset_class = NewsFilter
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['created_at']

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

        queryset = self.filter_queryset(self.get_queryset())

        serializer = ResponseSerializer({
            'code': 200,
            'status': 'success',
            'recordsTotal': queryset.count(),
            'data': NewsSerializer(self.queryset, many=True).data,
            'error': None,
        })

        return Response(serializer.data)


class CMSDetailNewsMediaViewSet(viewsets.ModelViewSet):
    queryset = DetailNewsMedia.objects.all()
    serializer_class = DetailNewsMediaSerializer
    permission_classes = [IsPengurus]
    filterset_fields = ['title', 'created_at', 'updated_at']
    filter_backends = [DjangoFilterBackend, KeywordOrderingFilter]
    filterset_class = NewsMediaFilter
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['created_at']

    def create(self, request, *args, **kwargs):
        super(CMSDetailNewsMediaViewSet, self).create(request, *args, **kwargs)

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

        detail_news_media = DetailNewsMedia.objects.get(id=request.query_params['id'])
        detail_news_media.delete()

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

        detail_news_media = DetailNewsMedia.objects.get(id=request.query_params['id'])
        serializer = self.get_serializer(detail_news_media, data=request.data, partial=True,
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

    def list(self, request, *args, **kwargs):
        if request.query_params.get('id'):
            detail_news_media = DetailNewsMedia.objects.get(id=request.query)
            serializer = ResponseSerializer({
                'code': 200,
                'status': 'success',
                'recordsTotal': 1,
                'data': DetailNewsMediaSerializer(detail_news_media).data,
                'error': None,
            })

            return Response(serializer.data)

        queryset = self.filter_queryset(self.get_queryset())

        serializer = ResponseSerializer({
            'code': 200,
            'status': 'success',
            'recordsTotal': queryset.count(),
            'data': DetailNewsMediaSerializer(queryset, many=True).data,
            'error': None,
        })

        return Response(serializer.data)
