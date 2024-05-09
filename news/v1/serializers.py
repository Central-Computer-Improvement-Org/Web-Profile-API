from django.utils import timezone
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from common.utils import rename_image_file
from news.detail_news_media_models import DetailNewsMedia
from news.models import News

import copy

class NewsSerializer(serializers.ModelSerializer):
    media_uri = serializers.ImageField(required=False)
    detail_news_media = serializers.ListField(child=serializers.CharField(), required=False)

    class Meta:
        model = News
        fields = [
            'id',
            'title',
            'description',
            'media_uri',
            'detail_news_media',
            'visited_count',
            'created_at',
            'updated_at',
            'created_by',
            'updated_by',
            'is_published',
        ]

        read_only_fields = [
            'id',
            'detail_news_media',
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
            new_data['media_uri'] = rename_image_file(new_data['media_uri'], prefix="NWS")

        if 'isPublished' in data:
            new_data['is_published'] = data.get('isPublished', None)

        if 'visitedCount' in data:
            new_data['visited_count'] = data.get('visitedCount', None)

        return super().to_internal_value(new_data)

    def to_representation(self, instance):
        response = super().to_representation(instance)

        response['mediaUri'] = response.pop('media_uri', None)
        response['createdAt'] = response.pop('created_at', None)
        response['updatedAt'] = response.pop('updated_at', None)
        response['createdBy'] = response.pop('created_by', None)
        response['updatedBy'] = response.pop('updated_by', None)
        response['isPublished'] = response.pop('is_published', None)
        response['visitedCount'] = response.pop('visited_count', None)
        response['detailNewsMedia'] = self.get_detail_news_media(instance)

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

    def get_detail_news_media(self, obj):
        detail_news_media = map(lambda x: "/media/" + x, DetailNewsMedia.objects.filter(news_id=obj.id).values_list('media_uri', flat=True))
        return detail_news_media


class DetailNewsMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailNewsMedia
        fields = [
            'id',
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
            'media_uri',
            'news_id',
        ]

    def to_internal_value(self, data):
        new_data = copy.deepcopy(data)

        if 'mediaUri' in data:
            new_data['media_uri'] = data.get('mediaUri', None)
            new_data['media_uri'] = rename_image_file(new_data['media_uri'], prefix="DNM")

        if 'newsId' in data:
            new_data['news_id'] = data.get('newsId', None)

        return super().to_internal_value(new_data)

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
            validated_data['media_uri'] = rename_image_file(validated_data['media_uri'], prefix="DNM")

        validated_data['updated_at'] = timezone.now()
        validated_data['updated_by'] = self.context['request'].user.nim

        return super(DetailNewsMediaSerializer, self).update(instance, validated_data)
