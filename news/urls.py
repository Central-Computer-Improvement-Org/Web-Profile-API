from django.urls import path

from news.v1.views import CMSNewsViewSet, PublicNewsViewSet, CMSDetailNewsMediaViewSet, PublicDetailNewsMediaViewSet, UpdateVisitedCount

cms_news_v1_urls = [
    path('', CMSNewsViewSet.as_view({'get': 'list', 'post': 'create', 'delete': 'destroy', 'patch': 'update'})),
    path('/detail-news-media', CMSDetailNewsMediaViewSet.as_view({'get': 'list', 'post': 'create', 'delete': 'destroy', 'patch': 'update'})),
    path('/visited-count', UpdateVisitedCount.as_view({'patch': 'update'})),
]

public_news_v1_urls = [
    path('', PublicNewsViewSet.as_view({'get': 'list'})),
    path('/detail-news-media', PublicDetailNewsMediaViewSet.as_view({'get': 'list'})),
]
