from django.urls import path, include

from .v1.views import SettingViewSet

urlpatterns_v1 = [
    path('cms/', include([
        path('setting/', SettingViewSet.as_view({
            'post': 'create',
            'put': 'update',
        }), name='setting'),
    ])),
    path('setting/', SettingViewSet.as_view({
        'get': 'retrieve',
    }), name='setting-detail'),
]
