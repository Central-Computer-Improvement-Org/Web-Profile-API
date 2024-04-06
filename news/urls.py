from django.urls import path

from news.v1.views import CMSNewsViewSet, PublicNewsViewSet

cms_news_v1_urls = [
    path('', CMSNewsViewSet.as_view({'get': 'list', 'post': 'create', 'delete': 'destroy', 'patch': 'update'})),
]

public_news_v1_urls = [
    path('', PublicNewsViewSet.as_view({'get': 'list'})),
]
