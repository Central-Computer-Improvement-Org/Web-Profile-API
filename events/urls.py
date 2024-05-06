from django.urls import path, include

from .v1.views import CMSEventViewSet, PublicEventViewSet

urlpatterns_v1_cms = [
    path('', CMSEventViewSet.as_view({
        'get': 'list',
        'post': 'create',
        'patch': 'update',
        'delete': 'destroy',
    }))
]

urlpatterns_v1_public = [
    path('', PublicEventViewSet.as_view({
        'get': 'list',
    }))
]
