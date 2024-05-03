from django.urls import path, include

from .v1.views import CMSAwardViewSet, PublicAwardViewSet

urlpatterns_v1_cms = [
    path('', CMSAwardViewSet.as_view({
        'get': 'list',
        'post': 'create',
        'patch': 'update',
        'delete': 'destroy',
    }))
]


urlpatterns_v1_public = [
    path('', PublicAwardViewSet.as_view({
        'get': 'list',
    }))
]
