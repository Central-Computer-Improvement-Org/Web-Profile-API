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

from users.urls import urlpatterns_v1_cms as userv1_cms_urls
from users.urls import urlpatterns_v1_public as userv1_urls
from auth.urls import urlpatterns_v1 as authv1_urls
from settings.urls import urlpatterns_v1_cms as settingv1_cms_urls
from settings.urls import urlpatterns_v1_public as settingv1_public_urls
from news.urls import cms_news_v1_urls, public_news_v1_urls
from projects.urls import urlpatterns_v1_cms as projectv1_cms_urls
from projects.urls import urlpatterns_v1_public as projectv1_public_urls


handler404 = "common.handler_views.error_404"


urlpatterns = [
    path('api/', include([
        path('v1/', include([
            path('cms/', include([
                path('users/', include(userv1_cms_urls)),
                path('settings/', include(settingv1_cms_urls)),
                path('news/', include(cms_news_v1_urls)),
                path('projects/', include(projectv1_cms_urls)),
            ])),
            path('users/', include(userv1_urls)),
            path('auth/', include(authv1_urls)),
            path('settings/', include(settingv1_public_urls)),
            path('news/', include(public_news_v1_urls)),
            path('projects/', include(projectv1_public_urls)),
        ])),
    ])),
]
