from django.urls import path

from auth.v1.views import JwtObtain, RegisterViewSet, RefreshToken


urlpatterns_v1 = [
    path('login/', JwtObtain.as_view(), name='token_obtain'),
    path('refresh/', RefreshToken.as_view(), name='token_refresh'),
    path('register/', RegisterViewSet.as_view({'post': 'create'}), name='register'),
]