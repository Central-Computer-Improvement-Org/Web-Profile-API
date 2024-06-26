from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.permissions import AllowAny, IsAuthenticated

from auth.auth import IsNotMember

from common.orderings import KeywordOrderingFilter
from common.utils import id_generator
from common.pagination import GenericPaginator

from copy import copy

from awards.v1.filtersets import AwardFilter, AwardSearchFilter

from generic_serializers.serializers import ResponseSerializer

from .serializers import AwardSerializer, DetailContributorAwardSerializer
from ..models import Award, DetailContributorAward

import json

class CMSAwardViewSet(viewsets.ModelViewSet):
    award_queryset = Award.objects.all()
    contributor_queryset = DetailContributorAward.objects.all()
    award_serializer_class = AwardSerializer
    contributor_serializer_class = DetailContributorAwardSerializer
    permission_classes = [IsNotMember]
    filterset_class = AwardFilter
    filter_backends = [DjangoFilterBackend, KeywordOrderingFilter, AwardSearchFilter]
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['created_at']
    pagination_class = GenericPaginator

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'list' or self.action == 'retrieve':
            return self.award_serializer_class
        else:
            return super().get_serializer_class()
        
    def get_queryset(self):
        return self.award_queryset

    def list(self, request, *args, **kwargs):
        if request.query_params.get('id'):
            if request.query_params.get('contributorsOnly') == 'true':
                if request.query_params.get('search'):
                    contributors = DetailContributorAward.objects.filter(Q(member_nim__name__icontains=request.query_params.get('search')) | Q(member_nim__nim__icontains=request.query_params.get('search')) & Q(award_id=request.query_params.get('id')))
                else:
                    contributors = DetailContributorAward.objects.filter(award_id=request.query_params.get('id'))

                page = self.paginate_queryset(contributors)

                serializer = ResponseSerializer({
                    'code': 200,
                    'status': 'success',
                    'recordsTotal': contributors.count(),
                    'data': DetailContributorAwardSerializer(page, many=True).data,
                    'error': None,
                })

                return Response(serializer.data)

            award = Award.objects.get(id=request.query_params.get('id'))

            serializer = ResponseSerializer({
                'code': 200,
                'status': 'success',
                'recordsTotal': 1,
                'data': AwardSerializer(award).data,
                'error': None,
            })

            return Response(serializer.data)

        queryset = self.filter_queryset(self.get_queryset().prefetch_related('contributors'))

        page = self.paginate_queryset(queryset)

        serializer = ResponseSerializer({
            'code': 200,
            'status': 'success',
            'recordsTotal': queryset.count(),
            'data': AwardSerializer(page, many=True).data,
            'error': None,
        })

        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        serializerAward = super(CMSAwardViewSet, self).create(request, *args, **kwargs)
        award_instance = serializerAward.data

        members = request.data.get('contributors')
        members_arr = []

        if members is not None and members is not '':
            members_arr = json.loads(members)
        
        if isinstance(members_arr, list) and len(members_arr) > 0:
            for member in members_arr:
                detail_contributor_data = {
                    'member_nim': member,
                    'award_id': award_instance['id'],  
                }

                detail_contributor_serializer = DetailContributorAwardSerializer(data=detail_contributor_data, context=self.get_serializer_context())

                if detail_contributor_serializer.is_valid():
                    detail_contributor_serializer.save()

        award = Award.objects.get(id=award_instance['id'])
                
        resp = ResponseSerializer({
            'code': 201,
            'status': 'success',
            'recordsTotal': 1,
            'data': {
                "message": "Created award successfully",
            },
            'error': None,
        })

        return Response(resp.data)
    
    def update(self, request, *args, **kwargs):
        id = request.query_params.get('id', None)

        if id is None:
            raise ValueError('ID is required')
        
        try:
            award = Award.objects.get(id=request.query_params['id'])
            award_serializer = self.get_serializer(instance=award, data=request.data, partial=True, context={'request': request})

            if not award_serializer.is_valid():
                raise ValidationError(award_serializer.errors)

            with transaction.atomic():
                award_serializer.save()

                members = request.data.get('contributors')

                members_arr = []

                if members is not None and members is not '':
                    members_arr = json.loads(members)
                
                if isinstance(members_arr, list) and len(members_arr) > 0:
                    DetailContributorAward.objects.filter(award_id=id).delete()
                    for member in members_arr:
                        detail_contributor_data = {
                            'member_nim': member,
                            'award_id': id,  
                        }
                        detail_contributor_serializer = DetailContributorAwardSerializer(data=detail_contributor_data, context=self.get_serializer_context())
                        if detail_contributor_serializer.is_valid():
                            detail_contributor_serializer.save()
                    
            resp = ResponseSerializer({
                'code': 200,
                'status': 'success',
                'recordsTotal': 1,
                'data': {
                    "message": "Updated award successfully",
                },
                'error': None,
            })

            return Response(resp.data, status=status.HTTP_200_OK)
        
        except Award.DoesNotExist:
            raise NotFound('Award does not exist!')
        
    def destroy(self, request, *args, **kwargs):
        id = request.query_params.get('id', None)

        if id is None:
            raise ValueError('ID is required')
        
        try:
            award = Award.objects.get(id=id)

            DetailContributorAward.objects.filter(award_id=id).delete()

            self.perform_destroy(award)

            resp = ResponseSerializer({
                'code': 200,
                'status': 'success',
                'recordsTotal': 0,
                'data': {
                    "message": "Deleted award successfully",
                },
                'error': None,
            })

            return Response(resp.data, status=status.HTTP_200_OK)
    
        except Award.DoesNotExist:
            raise NotFound('Award does not exist!')

class PublicAwardViewSet(viewsets.ModelViewSet):
    queryset = Award.objects.all()
    serializer_class = AwardSerializer
    permission_classes = [AllowAny]
    filterset_class = AwardFilter
    filter_backends = [DjangoFilterBackend, KeywordOrderingFilter, AwardSearchFilter]
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['created_at']
    pagination_class = GenericPaginator
    authentication_classes = []

    def list(self, request, *args, **kwargs):
        if request.query_params.get('id'):
            if request.query_params.get('contributorsOnly') == 'true':
                if request.query_params.get('search'):
                    contributors = DetailContributorAward.objects.filter(Q(member_nim__name__icontains=request.query_params.get('search')) | Q(member_nim__nim__icontains=request.query_params.get('search')) & Q(award_id=request.query_params.get('id')))
                else:
                    contributors = DetailContributorAward.objects.filter(award_id=request.query_params.get('id'))

                page = self.paginate_queryset(contributors)

                serializer = ResponseSerializer({
                    'code': 200,
                    'status': 'success',
                    'recordsTotal': contributors.count(),
                    'data': DetailContributorAwardSerializer(page, many=True).data,
                    'error': None,
                })

                return Response(serializer.data)

            award = Award.objects.get(id=request.query_params.get('id'))

            serializer = ResponseSerializer({
                'code': 200,
                'status': 'success',
                'recordsTotal': 1,
                'data': AwardSerializer(award).data,
                'error': None,
            })

            return Response(serializer.data)

        queryset = self.filter_queryset(self.get_queryset().prefetch_related('contributors'))

        page = self.paginate_queryset(queryset)

        serializer = ResponseSerializer({
            'code': 200,
            'status': 'success',
            'recordsTotal': queryset.count(),
            'data': AwardSerializer(page, many=True).data,
            'error': None,
        })

        return Response(serializer.data)