from django.urls import path, include

from .v1.views import CMSSettingViewSet, PublicSettingViewSet, CMSContactViewSet, PublicContactViewSet

urlpatterns_v1_cms = [
    path('/setting', CMSSettingViewSet.as_view({
        'get': 'retrieve',
        'patch': 'update',
    }), name='setting'),
    path('/contact', CMSContactViewSet.as_view({
        'get': 'list',
        'post': 'create',
        'patch': 'update',
        'delete': 'destroy',
    }), name='contact'),
]


urlpatterns_v1_public = [
    path('/setting', PublicSettingViewSet.as_view({
        'get': 'retrieve',
    }), name='setting-detail'),
    path('/contact', PublicContactViewSet.as_view({
        'get': 'list',
    }), name='setting-detail'),
]
