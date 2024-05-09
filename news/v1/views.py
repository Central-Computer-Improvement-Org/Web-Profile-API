import copy
import json
from datetime import datetime

from django.utils import timezone
from django_filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from auth.auth import IsNotMember
from common.orderings import KeywordOrderingFilter
from common.pagination import GenericPaginator
from common.utils import rename_image_file
from generic_serializers.serializers import ResponseSerializer
from news.detail_news_media_models import DetailNewsMedia
from news.news_models import News
from news.v1.filtersets import NewsFilter, NewsMediaFilter, NewsSearchFilter
from news.v1.serializers import NewsSerializer, DetailNewsMediaSerializer


class CMSNewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsNotMember]
    filter_backends = [DjangoFilterBackend, KeywordOrderingFilter, NewsSearchFilter]
    filterset_class = NewsFilter
    ordering_fields = ['createdAt', 'updatedAt']
    ordering = ['created_at']
    pagination_class = GenericPaginator

    def create(self, request, *args, **kwargs):
        #super(CMSNewsViewSet, self).create(request, *args, **kwargs)

        news_copy = copy.deepcopy(request.data)

        detail_news_media = None

        if 'detailNewsMedia' in news_copy:
            detail_news_media = news_copy.pop('detailNewsMedia')

        serializer = self.get_serializer(data=news_copy, context={'request': request})

        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        serializer.save()

        if detail_news_media is not None:
            dnms = []

            for media in detail_news_media:
                new_dnm = {
                    'newsId': serializer.data['id'],
                    'mediaUri': media
                }
                dnm_serializer = DetailNewsMediaSerializer(data=new_dnm, context={'request': request})

                if not dnm_serializer.is_valid():
                    raise ValidationError(dnm_serializer.errors)

                dnms.append(dnm_serializer)

            for dnm in dnms:
                dnm.save()

        serializer = ResponseSerializer({
            'code': 200,
            'status': 'success',
            'recordsTotal': 1,
            'data': {
                "message": "Created news successfully"
            },
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
            'data': {
                "message": "Deleted news successfully"
            },
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
            'data': {
                "message": "Updated news successfully"
            },
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

        page = self.paginate_queryset(queryset)

        serializer = ResponseSerializer({
            'code': 200,
            'status': 'success',
            'recordsTotal': queryset.count(),
            'data': NewsSerializer(page, many=True).data,
            'error': None,
        })

        return Response(serializer.data)


class PublicNewsViewSet(viewsets.ModelViewSet):
    serializer_class = NewsSerializer
    permission_classes = [AllowAny]
    queryset = News.objects.filter(is_published=True)
    filter_backends = [DjangoFilterBackend, KeywordOrderingFilter]
    filterset_class = NewsFilter
    ordering_fields = ['createdAt', 'updatedAt']
    ordering = ['created_at']
    pagination_class = GenericPaginator
    authentication_classes = []

    def list(self, request, *args, **kwargs):
        if request.query_params.get('id'):
            news = News.objects.get(id=request.query_params.get('id'))

            if news.is_published:
                serializer = ResponseSerializer({
                    'code': 200,
                    'status': 'success',
                    'recordsTotal': 1,
                    'data': NewsSerializer(news).data,
                    'error': None,
                })

                return Response(serializer.data)

            raise NotFound('News not found')

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)

        serializer = ResponseSerializer({
            'code': 200,
            'status': 'success',
            'recordsTotal': queryset.count(),
            'data': NewsSerializer(page, many=True).data,
            'error': None,
        })

        return Response(serializer.data)


class CMSDetailNewsMediaViewSet(viewsets.ModelViewSet):
    queryset = DetailNewsMedia.objects.all()
    serializer_class = DetailNewsMediaSerializer
    permission_classes = [IsNotMember]
    filterset_fields = ['title', 'created_at', 'updated_at']
    filter_backends = [DjangoFilterBackend, KeywordOrderingFilter]
    filterset_class = NewsMediaFilter
    ordering_fields = ['createdAt', 'updatedAt']
    ordering = ['created_at']
    pagination_class = GenericPaginator

    def create(self, request, *args, **kwargs):
        super(CMSDetailNewsMediaViewSet, self).create(request, *args, **kwargs)

        serializer = ResponseSerializer({
            'code': 200,
            'status': 'success',
            'recordsTotal': 1,
            'data': {
                "message": "Created detail news media successfully"
            },
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
            'data': {
                "message": "Deleted detail news media successfully"
            },
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
            'data': {
                "message": "Updated detail news media successfully"
            },
            'error': None,
        })

        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        if request.query_params.get('id'):
            detail_news_media = DetailNewsMedia.objects.get(id=request.query_params.get('id'))
            serializer = ResponseSerializer({
                'code': 200,
                'status': 'success',
                'recordsTotal': 1,
                'data': DetailNewsMediaSerializer(detail_news_media).data,
                'error': None,
            })

            return Response(serializer.data)

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)

        serializer = ResponseSerializer({
            'code': 200,
            'status': 'success',
            'recordsTotal': queryset.count(),
            'data': DetailNewsMediaSerializer(page, many=True).data,
            'error': None,
        })

        return Response(serializer.data)

class PublicDetailNewsMediaViewSet(viewsets.ModelViewSet):
    queryset = DetailNewsMedia.objects.all()
    serializer_class = DetailNewsMediaSerializer
    permission_classes = [AllowAny]
    filterset_fields = ['title', 'created_at', 'updated_at']
    filter_backends = [DjangoFilterBackend, KeywordOrderingFilter]
    filterset_class = NewsMediaFilter
    ordering_fields = ['createdAt', 'updatedAt']
    ordering = ['created_at']
    pagination_class = GenericPaginator
    authentication_classes = []

    def list(self, request, *args, **kwargs):
        if request.query_params.get('id'):
            detail_news_media = DetailNewsMedia.objects.get(id=request.query_params.get('id'))
            serializer = ResponseSerializer({
                'code': 200,
                'status': 'success',
                'recordsTotal': 1,
                'data': DetailNewsMediaSerializer(detail_news_media).data,
                'error': None,
            })

            return Response(serializer.data)

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)

        serializer = ResponseSerializer({
            'code': 200,
            'status': 'success',
            'recordsTotal': queryset.count(),
            'data': DetailNewsMediaSerializer(page, many=True).data,
            'error': None,
        })

        return Response(serializer.data)


class UpdateVisitedCount(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsNotMember]

    def update(self, request, *args, **kwargs):
        if request.query_params.get('id') is None:
            raise ValueError('ID is required')

        news = News.objects.get(id=request.query_params['id'])
        news.visited_count += 1
        news.save()

        serializer = ResponseSerializer({
            'code': 200,
            'status': 'success',
            'recordsTotal': 1,
            'data': {
                "message": "Updated visited count successfully"
            },
            'error': None,
        })

        return Response(serializer.data)