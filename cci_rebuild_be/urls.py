"""
URL configuration for cci_rebuild_be project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include

from users.urls import urlpatterns_v1 as userv1_urls
from auth.urls import urlpatterns_v1 as authv1_urls
from settings.urls import urlpatterns_v1 as settingv1_urls

urlpatterns = [
    path('api/', include([
        path('v1/', include(
            [
                path('users/', include(userv1_urls)),
                path('auth/', include(authv1_urls)),
                path('settings/', include(settingv1_urls))
            ]
        ))
    ])),
]
