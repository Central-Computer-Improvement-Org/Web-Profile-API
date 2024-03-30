from django.urls import path, include

from rest_framework_simplejwt.views import TokenRefreshView

from .views import JwtObtain, RegisterViewSet


urlpatterns_v1 = [
    path('login/', JwtObtain.as_view(), name='token_obtain'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterViewSet.as_view({'post': 'create'}), name='register'),
]