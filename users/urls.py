from django.urls import path, include

from .v1.views import UserProfileViewSet, UserViewSet

urlpatterns_v1 = [
    path('cms/', include([
        path('users/', UserViewSet.as_view({
            'get': 'list',
        }), name='users'),
    ])),
    path('profile/', UserProfileViewSet.as_view({
        'get': 'retrieve',
    }), name='profile'),
]
