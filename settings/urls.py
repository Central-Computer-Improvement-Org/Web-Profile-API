from django.urls import path, include

from .v1.views import SettingViewSet

urlpatterns_v1_cms = [
    path('setting/', SettingViewSet.as_view({
        'post': 'create',
        'put': 'update',
    }), name='setting'),
]


urlpatterns_v1_public = [
    path('setting/', SettingViewSet.as_view({
        'get': 'retrieve',
    }), name='setting-detail'),
]
