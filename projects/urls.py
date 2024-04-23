from django.urls import path, include

from .v1.views import CMSProjectViewSet, PublicProjectViewSet, CMSDetailContributorProjectViewSet, PublicDetailContributorProjectViewSet

urlpatterns_v1_cms = [
    path('', CMSProjectViewSet.as_view({
        'get': 'list',
        'post': 'create',
        'patch': 'update',
        'delete': 'destroy',
    }), name='project'),
    path('contributorDetails/', CMSDetailContributorProjectViewSet.as_view({
        'get': 'list',
        'post': 'create',
        'patch': 'update',
        'delete': 'destroy',
    }), name='detail-contributor-project'),
]


urlpatterns_v1_public = [
    path('', PublicProjectViewSet.as_view({
        'get': 'list',
    }), name='project-detail'),
    path('contributorDetails/', PublicDetailContributorProjectViewSet.as_view({
        'get': 'list',
    }), name='detail-contributor-project-detail'),
]
