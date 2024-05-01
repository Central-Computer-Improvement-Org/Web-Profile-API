from django.urls import path, include

from .v1.views import CMSProjectViewSet, PublicProjectViewSet

urlpatterns_v1_cms = [
    path('', CMSProjectViewSet.as_view({
        'get': 'list',
        'post': 'create',
        'patch': 'update',
        'delete': 'destroy',
    }))
]


urlpatterns_v1_public = [
    path('', PublicProjectViewSet.as_view({
        'get': 'list',
    }))
]
