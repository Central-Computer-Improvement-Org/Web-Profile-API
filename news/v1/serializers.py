from django.utils import timezone
from rest_framework import serializers

from news.detail_news_media import DetailNewsMedia
from news.models import News


class NewsSerializer(serializers.ModelSerializer):
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
        ]

    def to_internal_value(self, data):
        data['media_uri'] = data.get('mediaUri', None)

        return super().to_internal_value(data)

    def to_representation(self, instance):
        response = super().to_representation(instance)

        response['mediaUri'] = response.pop('media_uri', None)
        response['createdAt'] = response.pop('created_at', None)
        response['updatedAt'] = response.pop('updated_at', None)

        return response

    def create(self, validated_data):
        validated_data['id'] = f'NWS-{timezone.now().strftime("%Y%m%d%H%M%S%f")}'

        validated_data['created_by'] = self.context['request'].user.nim
        validated_data['updated_by'] = self.context['request'].user.nim

        return super(NewsSerializer, self).create(validated_data)


class DetailNewsMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailNewsMedia
        fields = '__all__'

    def to_internal_value(self, data):
        data['media_uri'] = data.get('mediaUri', None)
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
        validated_data['created_by'] = self.context['request'].user.nim
        validated_data['updated_by'] = self.context['request'].user.nim

        return super(DetailNewsMediaSerializer, self).create(validated_data)