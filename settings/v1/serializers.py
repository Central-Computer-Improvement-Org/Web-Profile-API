from rest_framework import serializers

from ..models import Setting, Contact

from common.utils import rename_image_file, delete_old_file, id_generator

import copy

class SettingSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Setting 
        fields = [
            'id',
            'name',
            'address',
            'description',
            'logo_uri',
            'title_website',
            'visited_count',
            'keyword',
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
            'address',
            'description',
            'logo_uri',
            'title_website',
            'keyword',
        ]

    def to_representation(self, instance):
        response = super().to_representation(instance)
        # rename all field to camelCase

        response['id'] = response.pop('id')
        response['name'] = response.pop('name')
        response['address'] = response.pop('address')
        response['description'] = response.pop('description')
        response['logoUri'] = response.pop('logo_uri')
        response['titleWebsite'] = response.pop('title_website')
        response['keyword'] = response.pop('keyword')
        response['visitedCount'] = response.pop('visited_count')
        response['createdAt'] = response.pop('created_at')
        response['updatedAt'] = response.pop('updated_at')
        response['createdBy'] = response.pop('created_by')
        response['updatedBy'] = response.pop('updated_by')

        return response

    def to_internal_value(self, data):
        new_data = copy.deepcopy(data)

        if 'visitedCount' in data:
            new_data['visited_count'] = data.get('visitedCount', None)

        if 'titleWebsite' in data:
            new_data['title_website'] = data.get('titleWebsite', None)

        if 'logoUri' in data :
            new_data['logo_uri'] = data.get('logoUri')
            new_data['logo_uri'] = rename_image_file(new_data['logo_uri'], prefix="STG")

        return super().to_internal_value(new_data)
    
    def update(self, instance, validated_data):
        if self.context['request'].user.is_authenticated:
            validated_data['updated_by'] = self.context['request'].user.nim
        else:
            validated_data['updated_by'] = "system"

        if 'logo_uri' in validated_data and validated_data['logo_uri']:
            old_logo_uri = instance.logo_uri.path if instance.logo_uri else None
            validated_data['logo_uri'] = rename_image_file(validated_data['logo_uri'], prefix="STG")

            if old_logo_uri and old_logo_uri != "uploads/setting/default.png":
                delete_old_file(old_logo_uri)

        return super(SettingSerializer, self).update(instance, validated_data)
    

class ContactSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Contact 
        fields = [
            'id',
            'platform',
            'account_uri',
            'icon_uri',
            'is_active',
            'value',
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
            'platform',
            'account_uri',
            'icon_uri',
        ]

    def to_representation(self, instance):
        response = super().to_representation(instance)
        # rename all field to camelCase

        response['id'] = response.pop('id')
        response['platform'] = response.pop('platform')
        response['accountUri'] = response.pop('account_uri')
        response['iconUri'] = response.pop('icon_uri')
        response['value'] = response.pop('value')
        response['isActive'] = response.pop('is_active')
        response['createdAt'] = response.pop('created_at')
        response['updatedAt'] = response.pop('updated_at')
        response['createdBy'] = response.pop('created_by')
        response['updatedBy'] = response.pop('updated_by')

        return response
    
    def to_internal_value(self, data):
        new_data = copy.deepcopy(data)

        if 'accountUri' in data:
            new_data['account_uri'] = data.get('accountUri', None)

        if 'isActive' in data:
            new_data['is_active'] = data.get('isActive', None)

        if 'iconUri' in data:
            new_data['icon_uri'] = data.get('iconUri', None)
            new_data['icon_uri'] = rename_image_file(new_data['icon_uri'], prefix="CNT")

        return super().to_internal_value(new_data)

    def create(self, validated_data):
        if validated_data['icon_uri'] is None:
            raise ValueError('Icon URI is required')

        validated_data['id'] = id_generator(prefix="CNT")

        validated_data['created_by'] = self.context['request'].user.nim
        validated_data['updated_by'] = self.context['request'].user.nim

        return super(ContactSerializer, self).create(validated_data)

    
    def update(self, instance, validated_data):
        if 'icon_uri' in validated_data:
            old_icon_uri = instance.icon_uri.path if instance.icon_uri else None
            validated_data['icon_uri'] = rename_image_file(validated_data['icon_uri'], prefix="PJTIC")

            delete_old_file(old_icon_uri)

        validated_data['updated_by'] = self.context['request'].user.nim

        return super(ContactSerializer, self).update(instance, validated_data)
    
    def delete_icon_uri(self, instance):
        old_icon_uri = str(instance.icon_uri) if instance.icon_uri else None

        if old_icon_uri:
            delete_old_file(old_icon_uri)