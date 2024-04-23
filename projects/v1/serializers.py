from rest_framework import serializers

from ..models import Project, DetailContributorProject

from common.utils import id_generator

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'id',
            'name',
            'description',
            'production_uri',
            'repository_uri',
            'budget',
            'created_at',
            'updated_at',
            'created_by',
            'updated_by',
        ]

        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
            'created_by',
            'updated_by',
        ]

        required_fields = [
            'name',
            'description',
            'production_uri',
            'repository_uri',
            'budget',
        ]

    def to_representation(self, instance):
        response = super().to_representation(instance)
        # rename all field to camelCase

        response['id'] = response.pop('id')
        response['name'] = response.pop('name')
        response['description'] = response.pop('description')
        response['productionUri'] = response.pop('production_uri')
        response['repositoryUri'] = response.pop('repository_uri')
        response['budget'] = response.pop('budget')
        response['createdAt'] = response.pop('created_at')
        response['updatedAt'] = response.pop('updated_at')
        response['createdBy'] = response.pop('created_by')
        response['updatedBy'] = response.pop('updated_by')

        return response
    
    def to_internal_value(self, data):
        data['name'] = data.get('name', self.instance.name if self.instance else None)
        data['description'] = data.get('description', self.instance.description if self.instance else None)
        data['production_uri'] = data.get('productionUri', self.instance.production_uri if self.instance else None)
        data['repository_uri'] = data.get('repositoryUri', self.instance.repository_uri if self.instance else None)
        data['budget'] = data.get('budget', self.instance.budget if self.instance else None)

        return super().to_internal_value(data)
    
    def create(self, validated_data):
        validated_data['id'] = id_generator(prefix="PJT")

        validated_data['created_by'] = self.context['request'].user.nim
        validated_data['updated_by'] = self.context['request'].user.nim

        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        validated_data['updated_by'] = self.context['request'].user.nim

        return super().update(instance, validated_data)
    
class DetailContributorProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailContributorProject
        fields = [
            'id',
            'member_nim',
            'project_id',
            'created_at',
            'updated_at',
            'created_by',
            'updated_by',
        ]

        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
            'created_by',
            'updated_by',
        ]

        required_fields = [
            'member_nim',
            'project_id',
        ]

    def to_representation(self, instance):
        response = super().to_representation(instance)
        # rename all field to camelCase

        response['id'] = response.pop('id')
        response['memberNim'] = response.pop('member_nim')
        response['projectId'] = response.pop('project_id')
        response['createdAt'] = response.pop('created_at')
        response['updatedAt'] = response.pop('updated_at')
        response['createdBy'] = response.pop('created_by')
        response['updatedBy'] = response.pop('updated_by')

        return response
    
    def to_internal_value(self, data):
        data['member_nim'] = data.get('memberNim', self.instance.member_nim if self.instance else None)
        data['project_id'] = data.get('projectId', self.instance.project_id if self.instance else None)

        return super().to_internal_value(data)
    
    def create(self, validated_data):
        validated_data['id'] = id_generator(prefix="DCP")

        validated_data['created_by'] = self.context['request'].user.nim
        validated_data['updated_by'] = self.context['request'].user.nim

        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        validated_data['updated_by'] = self.context['request'].user.nim

        return super().update(instance, validated_data)