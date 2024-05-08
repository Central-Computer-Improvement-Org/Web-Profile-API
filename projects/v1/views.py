from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.permissions import AllowAny, IsAuthenticated

from auth.auth import IsPengurus
from common.orderings import KeywordOrderingFilter
from common.pagination import GenericPaginator

from projects.v1.filtersets import ProjectFilter, ProjectSearchFilter

from generic_serializers.serializers import ResponseSerializer

from .serializers import ProjectSerializer, DetailContributorProjectSerializer
from ..models import Project, DetailContributorProject

import json

class CMSProjectViewSet(viewsets.ModelViewSet):
    project_queryset = Project.objects.all()
    contributor_queryset = DetailContributorProject.objects.all()
    project_serializer_class = ProjectSerializer
    contributor_serializer_class = DetailContributorProjectSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = ProjectFilter
    filter_backends = [DjangoFilterBackend, KeywordOrderingFilter, ProjectSearchFilter]
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['created_at']
    pagination_class = GenericPaginator

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'list' or self.action == 'retrieve':
            return self.project_serializer_class
        else:
            return super().get_serializer_class()
        
    def get_queryset(self):
        return self.project_queryset

    def list(self, request, *args, **kwargs):
        if request.query_params.get('id'):
            project = Project.objects.get(id=request.query_params.get('id'))

            serializer = ResponseSerializer({
                'code': 200,
                'status': 'success',
                'recordsTotal': 1,
                'data': ProjectSerializer(project).data,
                'error': None,
            })

            return Response(serializer.data)

        queryset = self.filter_queryset(self.get_queryset().prefetch_related('contributors'))

        page = self.paginate_queryset(queryset)

        serializer = ResponseSerializer({
            'code': 200,
            'status': 'success',
            'recordsTotal': queryset.count(),
            'data': ProjectSerializer(page, many=True).data,
            'error': None,
        })

        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        serializerProject = super(CMSProjectViewSet, self).create(request, *args, **kwargs)
        project_instance = serializerProject.data

        members = request.data.get('contributors')

        members_arr = json.loads(members)
        
        if members_arr is not []:
            for member in members_arr:
                detail_contributor_data = {
                    'member_nim': member,
                    'project_id': project_instance['id'],  
                }

                detail_contributor_serializer = DetailContributorProjectSerializer(data=detail_contributor_data, context=self.get_serializer_context())

                if detail_contributor_serializer.is_valid():
                    detail_contributor_serializer.save()

        project = Project.objects.get(id=project_instance['id'])
                
        resp = ResponseSerializer({
            'code': 201,
            'status': 'success',
            'recordsTotal': 1,
            'data': ProjectSerializer(project,many=False).data,
            'error': None,
        })

        return Response(resp.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        id = request.query_params.get('id', None)

        if id is None:
            raise ValueError('ID is required')
        
        try:
            project = Project.objects.get(id=request.query_params['id'])
            project_serializer = self.get_serializer(instance=project, data=request.data, partial=True, context={'request': request})

            if not project_serializer.is_valid():
                raise ValidationError(project_serializer.errors)

            with transaction.atomic():
                project_serializer.save()

                members = request.data.getlist('contributors')
                
                if len(members) > 0:
                    DetailContributorProject.objects.filter(project_id=id).delete()
                    for member in members:
                        detail_contributor_data = {
                            'member_nim': member,
                            'project_id': id,  
                        }
                        detail_contributor_serializer = DetailContributorProjectSerializer(data=detail_contributor_data, context=self.get_serializer_context())
                        if detail_contributor_serializer.is_valid():
                            detail_contributor_serializer.save()
                    
            resp = ResponseSerializer({
                'code': 204,
                'status': 'success',
                'recordsTotal': 1,
                'data': ProjectSerializer(project).data,
                'error': None,
            })

            return Response(resp.data, status=status.HTTP_204_NO_CONTENT)
        
        except Project.DoesNotExist:
            raise NotFound('Project does not exist!')
        
    def destroy(self, request, *args, **kwargs):
        id = request.query_params.get('id', None)

        if id is None:
            raise ValueError('ID is required')
        
        try:
            project = Project.objects.get(id=id)

            serializer = ProjectSerializer(project)

            serializer.delete_icon_uri(project)

            DetailContributorProject.objects.filter(project_id=id).delete()

            self.perform_destroy(project)

            resp = ResponseSerializer({
                'code': 204,
                'status': 'success',
                'recordsTotal': 0,
                'data': None,
                'error': None,
            })

            return Response(resp.data, status=status.HTTP_204_NO_CONTENT)
    
        except Project.DoesNotExist:
            raise NotFound('Project does not exist!')

class PublicProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [AllowAny]
    filterset_class = ProjectFilter
    filter_backends = [DjangoFilterBackend, KeywordOrderingFilter, ProjectSearchFilter]
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['created_at']
    pagination_class = GenericPaginator

    def list(self, request, *args, **kwargs):
        if request.query_params.get('id'):
            project = Project.objects.get(id=request.query_params.get('id'))

            serializer = ResponseSerializer({
                'code': 200,
                'status': 'success',
                'recordsTotal': 1,
                'data': ProjectSerializer(project).data,
                'error': None,
            })

            return Response(serializer.data)

        queryset = self.filter_queryset(self.get_queryset().prefetch_related('contributors'))

        page = self.paginate_queryset(queryset)

        serializer = ResponseSerializer({
            'code': 200,
            'status': 'success',
            'recordsTotal': queryset.count(),
            'data': ProjectSerializer(page, many=True).data,
            'error': None,
        })

        return Response(serializer.data)