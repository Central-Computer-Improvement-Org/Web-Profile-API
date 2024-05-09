from datetime import datetime

from django.utils import timezone
from rest_framework import serializers

from common.utils import rename_image_file
from events.models import Event
from users.v1.serializers import DivisionSerializer


class EventSerializer(serializers.ModelSerializer):
    division = DivisionSerializer(source="division_id", read_only=True)
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
            'name',
            'description',
            'is_active',
        ]

    def to_representation(self, instance):
        response = super().to_representation(instance)

        response['divisionId'] = response.pop('division_id', None)
        response['division'] = response.pop('division', None)
        response['createdAt'] = response.pop('created_at', None)
        response['updatedAt'] = response.pop('updated_at', None)
        response['createdBy'] = response.pop('created_by', None)
        response['updatedBy'] = response.pop('updated_by', None)
        response['isActive'] = response.pop('is_active', None)
        response['mediaUri'] = response.pop('media_uri', None)
        response['heldOn'] = response.pop('held_on', None)

        return response

    def to_internal_value(self, data):
        new_data = data.copy()

        if 'isActive' in data:
            new_data['is_active'] = data.get('isActive', None)

        if 'divisionId' in data:
            new_data['division_id'] = data.get('divisionId', None)

        if 'heldOn' in data:
            new_data['held_on'] = data.get('heldOn', None)
            new_data['held_on'] = datetime.strptime(new_data['held_on'], '%d-%m-%Y').date()

        if 'mediaUri' in data:
            new_data['media_uri'] = data.get('mediaUri', None)
            new_data['media_uri'] = rename_image_file(new_data['media_uri'], prefix="EVT")

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
        instance.is_active = False
        instance.save()

        return instance
