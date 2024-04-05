from django.urls import path, include

from rest_framework import routers

from .v1.views import UserProfileViewSet, UserViewSet, CMSDivisionViewSet, PublicDivisionViewSet

urlpatterns_v1_cms = [
    path('', UserViewSet.as_view({
        'get': 'list',
    }), name='users'),

    path("divisions/", CMSDivisionViewSet.as_view({
        'get': 'list',
        'delete': 'destroy',
        'post': 'create',
        'patch': 'update',
    }), name='cms_divisions'),
]

urlpatterns_v1_public = [
    path('profile/', UserProfileViewSet.as_view({
        'get': 'retrieve',
    }), name='profile'),
    path('divisions/', PublicDivisionViewSet.as_view({
        'get': 'list',
    }), name='divisions'),
]
