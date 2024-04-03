from rest_framework import serializers

from ..models import Setting, Contact

from common.utils import rename_image_file

class SettingSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Setting 
        fields = [
            'id',
            'name',
            'address',
            'telp',
            'description',
            'logo_uri',
            'title_website',
            'keyword',
            'created_at',
            'updated_at',
        ]

    def to_representation(self, instance):
        response = super().to_representation(instance)
        # rename all field to camelCase

        response['id'] = response.pop('id')
        response['name'] = response.pop('name')
        response['address'] = response.pop('address')
        response['telp'] = response.pop('telp')
        response['description'] = response.pop('description')
        response['logoUri'] = response.pop('logo_uri')
        response['titleWebsite'] = response.pop('title_website')
        response['keyword'] = response.pop('keyword')
        response['createdAt'] = response.pop('created_at')
        response['updatedAt'] = response.pop('updated_at')

        return response

    def to_internal_value(self, data):
        data['name'] = data.get('name', None)
        data['address'] = data.get('address', None)
        data['telp'] = data.get('telp', None)
        data['description'] = data.get('description', None)
        data['logo_uri'] = data.get('logoUri', None)
        data['title_website'] = data.get('titleWebsite', None)
        data['keyword'] = data.get('keyword', None)

        return super().to_internal_value(data)
    

class ContactSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Contact 
        fields = [
            'id',
            'platform',
            'icon_uri',
            'value',
            'visited_count',
            'is_active',
            'created_at',
            'updated_at',
        ]

    def to_representation(self, instance):
        response = super().to_representation(instance)
        # rename all field to camelCase

        response['id'] = response.pop('id')
        response['platform'] = response.pop('platform')
        response['iconUri'] = response.pop('icon_uri')
        response['value'] = response.pop('value')
        response['visitedCount'] = response.pop('visited_count')
        response['isActive'] = response.pop('is_active')
        response['createdAt'] = response.pop('created_at')
        response['updatedAt'] = response.pop('updated_at')

        return response
    
    def to_internal_value(self, data):
        data['platform'] = data.get('platform', None)
        data['icon_uri'] = data.get('iconUri', None)
        data['value'] = data.get('value', None)
        data['is_active'] = data.get('isActive', None)
        data['visited_count'] = data.get('visitedCount', None)

        return super().to_internal_value(data)