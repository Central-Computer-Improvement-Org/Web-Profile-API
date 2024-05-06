from django.utils import timezone
from rest_framework import serializers

from events.models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

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
            'start_date',
            'end_date',
            'is_published',
        ]

    def to_representation(self, instance):
        response = super().to_representation(instance)

        response['startDate'] = response.pop('start_date', None)
        response['endDate'] = response.pop('end_date', None)
        response['createdAt'] = response.pop('created_at', None)
        response['updatedAt'] = response.pop('updated_at', None)
        response['createdBy'] = response.pop('created_by', None)
        response['updatedBy'] = response.pop('updated_by', None)
        response['isPublished'] = response.pop('is_published', None)

        return response

    def to_internal_value(self, data):
        new_data = data.copy()

        if 'isPublished' in data:
            new_data['is_published'] = data.get('isPublished', None)

        if 'startDate' in data:
            new_data['start_date'] = data.get('startDate', None)

        if 'endDate' in data:
            new_data['end_date'] = data.get('endDate', None)

        return super().to_internal_value(new_data)

    def create(self, validated_data):
        validated_data['id'] = f'EVT-{timezone.now().strftime("%Y%m%d%H%M%S%f")}'

        validated_data['created_by'] = self.context['request'].user.nim
        validated_data['updated_by'] = self.context['request'].user.nim

        return super(EventSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        validated_data['updated_at'] = timezone.now()
        validated_data['updated_by'] = self.context['request'].user.nim

        return super(EventSerializer, self).update(instance, validated_data)

    def delete(self, instance):
        instance.is_published = False
        instance.save()

        return instance
