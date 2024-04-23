from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.permissions import IsAuthenticated, AllowAny

from auth.auth import IsPengurus
from common.orderings import KeywordOrderingFilter

from generic_serializers.serializers import ResponseSerializer

from .serializers import ProjectSerializer, DetailContributorProjectSerializer
from ..models import Project, DetailContributorProject

class CMSProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['name', 'created_at', 'updated_at']
    filter_backends = [DjangoFilterBackend, KeywordOrderingFilter]
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['created_at']

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

        queryset = self.filter_queryset(self.get_queryset())

        serializer = ResponseSerializer({
            'code': 200,
            'status': 'success',
            'recordsTotal': queryset.count(),
            'data': ProjectSerializer(queryset, many=True).data,
            'error': None,
        })

        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        serializer = self.get_serializer(data=data)
        detail_contributor_serializer = DetailContributorProjectSerializer(data=data.get('detailContributors', []), many=True)

        if not serializer.is_valid():
            raise ValidationError(serializer.errors)
        
        if not detail_contributor_serializer.is_valid():
            raise ValidationError(detail_contributor_serializer.errors)
        
        self.perform_create(serializer)

        project_instance = serializer.instance
        for detail_contributor_data in detail_contributor_serializer.validated_data:
            detail_contributor_data['project_id'] = project_instance.id
        detail_contributors = DetailContributorProject.objects.bulk_create([DetailContributorProject(**data) for data in detail_contributor_serializer.validated_data])

        project_data = project_serializer.data
        project_data['detail_contributors'] = [serializer.data for serializer in detail_contributor_serializer]

        
        resp = ResponseSerializer({
            'code': 201,
            'status': 'success',
            'recordsTotal': 1,
            'data': serializer.data,
            'error': None,
        })

        return Response(resp.data)
    
    def update(self, request, *args, **kwargs):
        id = request.query_params.get('id', None)

        if id is None:
            raise ValueError('ID is required')
        
        try:
            project = Project.objects.get(id=id)
            data = request.data.copy()
            serializer = self.get_serializer(project, data=data, partial=True)

            if not serializer.is_valid():
                raise ValidationError(serializer.errors)
            
            self.perform_update(serializer)
                    
            resp = ResponseSerializer({
                'code': 204,
                'status': 'success',
                'recordsTotal': 1,
                'data': ProjectSerializer(project).data,
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

            self.perform_destroy(project)

            resp = ResponseSerializer({
                'code': 204,
                'status': 'success',
                'recordsTotal': 0,
                'data': None,
                'error': None,
            })

            return Response(resp.data)
    
        except Project.DoesNotExist:
            raise NotFound('Project does not exist!')

class PublicProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [AllowAny]

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

        projects = Project.objects.all()

        serializer = ResponseSerializer({
            'code': 200,
            'status': 'success',
            'recordsTotal': projects.count(),
            'data': ProjectSerializer(projects, many=True).data,
            'error': None,
        })

        return Response(serializer.data)

class CMSDetailContributorProjectViewSet(viewsets.ModelViewSet):
    queryset = DetailContributorProject.objects.all()
    serializer_class = DetailContributorProjectSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['member_nim', 'project_id', 'created_at', 'updated_at']
    filter_backends = [DjangoFilterBackend, KeywordOrderingFilter]
    ordering_fields = ['member_nim', 'project_id', 'created_at', 'updated_at']
    ordering = ['created_at']

    def list(self, request, *args, **kwargs):
        if request.query_params.get('id'):
            detailContributorProject = DetailContributorProject.objects.get(id=request.query_params.get('id'))

            serializer = ResponseSerializer({
                'code': 200,
                'status': 'success',
                'recordsTotal': 1,
                'data': ProjectSerializer(detailContributorProject).data,
                'error': None,
            })

            return Response(serializer.data)

        queryset = self.filter_queryset(self.get_queryset())

        serializer = ResponseSerializer({
            'code': 200,
            'status': 'success',
            'recordsTotal': queryset.count(),
            'data': DetailContributorProjectSerializer(queryset, many=True).data,
            'error': None,
        })

        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        serializer = self.get_serializer(data=data)

        if not serializer.is_valid():
            raise ValidationError(serializer.errors)
        
        self.perform_create(serializer)
        
        resp = ResponseSerializer({
            'code': 201,
            'status': 'success',
            'recordsTotal': 1,
            'data': serializer.data,
            'error': None,
        })

        return Response(resp.data)
    
    def update(self, request, *args, **kwargs):
        id = request.query_params.get('id', None)

        if id is None:
            raise ValueError('ID is required')
        
        try:
            detailContributorProject = DetailContributorProject.objects.get(id=id)
            data = request.data.copy()
            serializer = self.get_serializer(detailContributorProject, data=data, partial=True)

            if not serializer.is_valid():
                raise ValidationError(serializer.errors)
            
            self.perform_update(serializer)
                    
            resp = ResponseSerializer({
                'code': 204,
                'status': 'success',
                'recordsTotal': 1,
                'data': ProjectSerializer(detailContributorProject).data,
                'error': None,
            })

            return Response(resp.data)
        
        except DetailContributorProject.DoesNotExist:
            raise NotFound('Detail Contributor Project does not exist!')
        
    def destroy(self, request, *args, **kwargs):
        if request.query_params.get('id'):
            try:
                id = request.query_params.get('id')
                detailContributorProject = DetailContributorProject.objects.get(id=id)

                self.perform_destroy(detailContributorProject)

                resp = ResponseSerializer({
                    'code': 204,
                    'status': 'success',
                    'recordsTotal': 0,
                    'data': None,
                    'error': None,
                })

                return Response(resp.data)
        
            except DetailContributorProject.DoesNotExist:
                raise NotFound('Detail Contributor Project does not exist!')
        elif request.query_params.get('memberNim'):
            try:
                member_nim = request.query_params.get('memberNim')
                detailContributorProjects = DetailContributorProject.objects.get(member_nim=member_nim)

                self.perform_destroy(detailContributorProjects)

                resp = ResponseSerializer({
                    'code': 204,
                    'status': 'success',
                    'recordsTotal': 0,
                    'data': None,
                    'error': None,
                })

                return Response(resp.data)
        
            except DetailContributorProject.DoesNotExist:
                raise NotFound('Detail Contributor Project does not exist!')
            
        elif request.query_params.get('projectId'):
            try:
                project_id = request.query_params.get('projectId')
                detailContributorProjects = DetailContributorProject.objects.get(project_id=project_id)

                self.perform_destroy(detailContributorProjects)

                resp = ResponseSerializer({
                    'code': 204,
                    'status': 'success',
                    'recordsTotal': 0,
                    'data': None,
                    'error': None,
                })

                return Response(resp.data)
        
            except DetailContributorProject.DoesNotExist:
                raise NotFound('Detail Contributor Project does not exist!')
            
        else:
            raise ValueError('id/projectId/memberNim is required')

        
class PublicDetailContributorProjectViewSet(viewsets.ModelViewSet):
    serializer_class = DetailContributorProjectSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        if request.query_params.get('id'):
            detailContributorProject = DetailContributorProject.objects.get(id=request.query_params.get('id'))

            serializer = ResponseSerializer({
                'code': 200,
                'status': 'success',
                'recordsTotal': 1,
                'data': DetailContributorProjectSerializer(detailContributorProject).data,
                'error': None,
            })

            return Response(serializer.data)

        detailContributorProjects = DetailContributorProject.objects.all()

        serializer = ResponseSerializer({
            'code': 200,
            'status': 'success',
            'recordsTotal': detailContributorProjects.count(),
            'data': DetailContributorProjectSerializer(detailContributorProjects, many=True).data,
            'error': None,
        })

        return Response(serializer.data)