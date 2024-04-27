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

        return super().to_internal_value(new_data)