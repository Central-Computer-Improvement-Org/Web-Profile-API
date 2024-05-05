from rest_framework import serializers

from ..models import Project, DetailContributorProject

from users.v1.serializers import UserSerializer

from common.utils import id_generator, rename_image_file, delete_old_file

import copy

class DetailContributorProjectSerializer(serializers.ModelSerializer):
    user = UserSerializer(source='member_nim', read_only=True)

    class Meta:
        model = DetailContributorProject
        fields = [
            'user',
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

        user_data = response.pop('user')
        response.update(user_data)

        response.pop('id', None)
        response.pop('project_id', None)
        response.pop('member_nim', None)
        response.pop('created_at', None)
        response.pop('updated_at', None)
        response.pop('created_by', None)
        response.pop('updated_by', None)
        
        return response
    
    def to_internal_value(self, data):

        return super().to_internal_value(data)
    
    def create(self, validated_data):
        validated_data['id'] = id_generator(prefix="DCP")

        validated_data['created_by'] = self.context['request'].user.nim
        validated_data['updated_by'] = self.context['request'].user.nim

        return super(DetailContributorProjectSerializer, self).create(validated_data)
    
    def update(self, instance, validated_data):
        validated_data['updated_by'] = self.context['request'].user.nim

        return super(DetailContributorProjectSerializer, self).update(instance, validated_data)

class ProjectSerializer(serializers.ModelSerializer):
    contributors = DetailContributorProjectSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            'id',
            'name',
            'description',
            'production_uri',
            'repository_uri',
            'image_uri',
            'icon_uri',
            'budget',
            'created_at',
            'updated_at',
            'created_by',
            'updated_by',
            'contributors'
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
        ]

    def to_representation(self, instance):
        response = super().to_representation(instance)
        # rename all field to camelCase

        response['id'] = response.pop('id')
        response['name'] = response.pop('name')
        response['description'] = response.pop('description')
        response['productionUri'] = response.pop('production_uri')
        response['repositoryUri'] = response.pop('repository_uri')
        response['imageUri'] = response.pop('image_uri')
        response['iconUri'] = response.pop('icon_uri')
        response['budget'] = response.pop('budget')
        response['contributors'] = response.pop('contributors')
        response['createdAt'] = response.pop('created_at')
        response['updatedAt'] = response.pop('updated_at')
        response['createdBy'] = response.pop('created_by')
        response['updatedBy'] = response.pop('updated_by')

        return response
    
    def to_internal_value(self, data):
        new_data = copy.deepcopy(data)
        
        if 'productionUri' in data:
            new_data['production_uri'] = data.get('productionUri', None)

        if 'repositoryUri' in data:
            new_data['repository_uri'] = data.get('repositoryUri', None)

        if 'iconUri' in data:
            new_data['icon_uri'] = data.get('iconUri', None)
            new_data['icon_uri'] = rename_image_file(new_data['icon_uri'], prefix="PJTIC")

        if 'imageUri' in data:
            new_data['image_uri'] = data.get('imageUri', None)
            new_data['image_uri'] = rename_image_file(new_data['image_uri'], prefix="PJTIMG")

        return super().to_internal_value(new_data)
    
    def create(self, validated_data):
        if validated_data['icon_uri'] is None:
            raise ValueError('Icon URI is required')
        
        if validated_data['image_uri'] is None:
            raise ValueError('Image URI is required')
        
        validated_data['id'] = id_generator(prefix="PJT")

        validated_data['created_by'] = self.context['request'].user.nim
        validated_data['updated_by'] = self.context['request'].user.nim

        return super(ProjectSerializer, self).create(validated_data)
    
    def update(self, instance, validated_data):
        if 'icon_uri' in validated_data:
            old_icon_uri = instance.icon_uri.path if instance.icon_uri else None
            validated_data['icon_uri'] = rename_image_file(validated_data['icon_uri'], prefix="PJTIC")

            delete_old_file(old_icon_uri)

        if 'image_uri' in validated_data:
            old_image_uri = instance.image_uri.path if instance.image_uri else None
            validated_data['image_uri'] = rename_image_file(validated_data['image_uri'], prefix="PJTIMG")

            delete_old_file(old_image_uri)
            
        validated_data['updated_by'] = self.context['request'].user.nim

        return super(ProjectSerializer, self).update(instance, validated_data)
    
    def delete_icon_uri(self, instance):
        old_icon_uri = str(instance.icon_uri) if instance.icon_uri else None

        old_image_uri = str(instance.image_uri) if instance.image_uri else None

        if old_icon_uri:
            delete_old_file(old_icon_uri)

        if old_image_uri:
            delete_old_file(old_image_uri)
    
