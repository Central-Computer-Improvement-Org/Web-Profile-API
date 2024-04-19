from django.utils import timezone
from rest_framework import serializers

from common.utils import rename_image_file
from news.detail_news_media import DetailNewsMedia
from news.models import News

import copy

class NewsSerializer(serializers.ModelSerializer):
    media_uri = serializers.ImageField(required=False)

    class Meta:
        model = News
        fields = [
            'id',
            'title',
            'description',
            'media_uri',
            'created_at',
            'updated_at',
            'created_by',
            'updated_by',
            'is_published',
        ]

        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
            'created_by',
            'updated_by',
        ]

        required_fields = [
            'title',
            'description',
        ]

    def to_internal_value(self, data):
        new_data = copy.deepcopy(data)

        if 'mediaUri' in data:
            new_data['media_uri'] = data.get('mediaUri', None)
            new_data['media_uri'] = rename_image_file(data['media_uri'], prefix="NWS")

        if 'isPublished' in data:
            new_data['is_published'] = data.get('isPublished', None)

        return super().to_internal_value(new_data)

    def to_representation(self, instance):
        response = super().to_representation(instance)

        response['mediaUri'] = response.pop('media_uri', None)
        response['createdAt'] = response.pop('created_at', None)
        response['updatedAt'] = response.pop('updated_at', None)
        response['createdBy'] = response.pop('created_by', None)
        response['updatedBy'] = response.pop('updated_by', None)
        response['isPublished'] = response.pop('is_published', None)

        return response

    def create(self, validated_data):
        if validated_data['media_uri'] is None:
            raise ValueError('Media URI is required')

        validated_data['id'] = f'NWS-{timezone.now().strftime("%Y%m%d%H%M%S%f")}'

        validated_data['created_by'] = self.context['request'].user.nim
        validated_data['updated_by'] = self.context['request'].user.nim

        return super(NewsSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        if 'media_uri' in validated_data:
            validated_data['media_uri'] = rename_image_file(validated_data['media_uri'], prefix="NWS")

        validated_data['updated_at'] = timezone.now()
        validated_data['updated_by'] = self.context['request'].user.nim

        return super(NewsSerializer, self).update(instance, validated_data)


class DetailNewsMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailNewsMedia
        fields = [
            'id',
            'title',
            'description',
            'media_uri',
            'news_id',
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
            'title',
            'description',
            'media_uri',
            'news_id',
        ]

    def to_internal_value(self, data):
        if 'mediaUri' in data:
            data['media_uri'] = data.get('mediaUri', None)
            data['media_uri'] = rename_image_file(data['media_uri'], prefix="STG")

        data['news_id'] = data.get('newsId', None)

        return super().to_internal_value(data)

    def to_representation(self, instance):
        response = super().to_representation(instance)

        response['newsId'] = response.pop('news_id')
        response['mediaUri'] = response.pop('media_uri')
        response['createdAt'] = response.pop('created_at')
        response['updatedAt'] = response.pop('updated_at')

        return response

    def create(self, validated_data):
        validated_data['id'] = f'DNM-{timezone.now().strftime("%Y%m%d%H%M%S%f")}'

        validated_data['created_by'] = self.context['request'].user.nim
        validated_data['updated_by'] = self.context['request'].user.nim

        return super(DetailNewsMediaSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        if 'media_uri' in validated_data:
            validated_data['media_uri'] = rename_image_file(validated_data['media_uri'], prefix="STG")

        validated_data['updated_at'] = timezone.now()
        validated_data['updated_by'] = self.context['request'].user.nim

        return super(DetailNewsMediaSerializer, self).update(instance, validated_data)
