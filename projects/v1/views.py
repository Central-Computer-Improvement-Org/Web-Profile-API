from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.permissions import AllowAny

from auth.auth import IsNotMember
from common.orderings import KeywordOrderingFilter
from common.pagination import GenericPaginator

from projects.v1.filtersets import ProjectFilter, ProjectSearchFilter

from generic_serializers.serializers import ResponseSerializer

from .serializers import ProjectSerializer, DetailContributorProjectSerializer, DetailDivisionProjectSerializer
from ..models import Project, DetailContributorProject, DetailDivisionProject

import json

class CMSProjectViewSet(viewsets.ModelViewSet):
    project_queryset = Project.objects.all()
    contributor_queryset = DetailContributorProject.objects.all()
    project_serializer_class = ProjectSerializer
    contributor_serializer_class = DetailContributorProjectSerializer
    division_serializer_class = DetailDivisionProjectSerializer
    permission_classes = [IsNotMember]
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
            if request.query_params.get('contributorsOnly') == "true":
                contributors = DetailContributorProject.objects.filter(project_id=request.query_params.get('id'))

                page = self.paginate_queryset(contributors)

                serializer = ResponseSerializer({
                    'code': 200,
                    'status': 'success',
                    'recordsTotal': contributors.count(),
                    'data': DetailContributorProjectSerializer(page, many=True).data,
                    'error': None,
                })

                return Response(serializer.data)
            
            project = Project.objects.get(id=request.query_params.get('id'))

            serializer = ResponseSerializer({
                'code': 200,
                'status': 'success',
                'recordsTotal': 1,
                'data': ProjectSerializer(project).data,
                'error': None,
            })

            return Response(serializer.data)

        queryset = self.filter_queryset(self.get_queryset().prefetch_related('contributors', 'divisions'))

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
        divisions = request.data.get('divisions')

        members_arr = []
        divisions_arr = []

        if divisions is not None and divisions is not '':
            divisions_arr = json.loads(divisions)

        if isinstance(divisions_arr, list) and len(divisions_arr) > 0:
            for division in divisions_arr:
                detail_division_data = {
                    'division_id': division,
                    'project_id': project_instance['id'],  
                }

                detail_division_serializer = DetailDivisionProjectSerializer(data=detail_division_data, context=self.get_serializer_context())

                if detail_division_serializer.is_valid():
                    detail_division_serializer.save()

        if members is not None and members is not '':
            members_arr = json.loads(members)
        
        if isinstance(members_arr, list) and len(members_arr) > 0:
            for member in members_arr:
                detail_contributor_data = {
                    'member_nim': member,
                    'project_id': project_instance['id'],  
                }

                detail_contributor_serializer = DetailContributorProjectSerializer(data=detail_contributor_data, context=self.get_serializer_context())

                if detail_contributor_serializer.is_valid():
                    detail_contributor_serializer.save()

        resp = ResponseSerializer({
            'code': 201,
            'status': 'success',
            'recordsTotal': 1,
            'data': {
                "message": "Created project successfully",
            },
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

                members = request.data.get('contributors')
                divisions = request.data.get('divisions')

                members_arr = []
                divisions_arr = []

                if divisions is not None and divisions is not '':
                    divisions_arr = json.loads(divisions)

                if isinstance(divisions_arr, list) and len(divisions_arr) > 0:
                    DetailDivisionProject.objects.filter(project_id=id).delete()
                    for division in divisions_arr:
                        detail_division_data = {
                            'division_id': division,
                            'project_id': id,  
                        }
                        detail_division_serializer = DetailDivisionProjectSerializer(data=detail_division_data, context=self.get_serializer_context())
                        if detail_division_serializer.is_valid():
                            detail_division_serializer.save()

                if members is not None and members is not '':
                    members_arr = json.loads(members)
                
                if isinstance(members_arr, list) and len(members_arr) > 0:
                    DetailContributorProject.objects.filter(project_id=id).delete()
                    for member in members_arr:
                        detail_contributor_data = {
                            'member_nim': member,
                            'project_id': id,  
                        }
                        detail_contributor_serializer = DetailContributorProjectSerializer(data=detail_contributor_data, context=self.get_serializer_context())
                        if detail_contributor_serializer.is_valid():
                            detail_contributor_serializer.save()
                    
            resp = ResponseSerializer({
                'code': 200,
                'status': 'success',
                'recordsTotal': 1,
                'data': {
                    "message": "Updated project successfully"
                },
                'error': None,
            })

            return Response(resp.data)
        
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
            DetailDivisionProject.objects.filter(project_id=id).delete()

            self.perform_destroy(project)

            resp = ResponseSerializer({
                'code': 200,
                'status': 'success',
                'recordsTotal': 0,
                'data': {
                    "message": "Deleted project successfully"
                },
                'error': None,
            })

            return Response(resp.data)
    
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
    authentication_classes = []

    def list(self, request, *args, **kwargs):
        if request.query_params.get('id'):
            if request.query_params.get('contributorsOnly') == "true":
                contributors = DetailContributorProject.objects.filter(project_id=request.query_params.get('id'))

                page = self.paginate_queryset(contributors)

                serializer = ResponseSerializer({
                    'code': 200,
                    'status': 'success',
                    'recordsTotal': contributors.count(),
                    'data': DetailContributorProjectSerializer(page, many=True).data,
                    'error': None,
                })

                return Response(serializer.data)
            
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