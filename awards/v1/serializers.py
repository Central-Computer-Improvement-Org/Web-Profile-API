from rest_framework import serializers

from ..models import Award, DetailContributorAward

from users.v1.serializers import UserSerializer

from common.utils import id_generator

import copy

class DetailContributorAwardSerializer(serializers.ModelSerializer):
    user = UserSerializer(source='member_nim', read_only=True)

    class Meta:
        model = DetailContributorAward
        fields = [
            'user',
            'id',
            'member_nim',
            'award_id',
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
            'award_id',
        ]

    def to_representation(self, instance):
        response = super().to_representation(instance)
        # rename all field to camelCase

        user_data = response.pop('user')
        response.update(user_data)

        response.pop('id', None)
        response.pop('award_id', None)
        response.pop('member_nim', None)
        response.pop('created_at', None)
        response.pop('updated_at', None)
        response.pop('created_by', None)
        response.pop('updated_by', None)

        return response
    
    def to_internal_value(self, data):

        return super().to_internal_value(data)
    
    def create(self, validated_data):
        validated_data['id'] = id_generator(prefix="DCA")

        validated_data['created_by'] = self.context['request'].user.nim
        validated_data['updated_by'] = self.context['request'].user.nim

        return super(DetailContributorAwardSerializer, self).create(validated_data)
    
    def update(self, instance, validated_data):
        validated_data['updated_by'] = self.context['request'].user.nim

        return super(DetailContributorAwardSerializer, self).update(instance, validated_data)
    
class AwardSerializer(serializers.ModelSerializer):
    contributors = DetailContributorAwardSerializer(many=True, read_only=True)

    class Meta:
        model = Award
        fields = [
            'id',
            'issuer',
            'title',
            'description',
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
            'issuer',
            'title',
            'description',
        ]

    def to_representation(self, instance):
        response = super().to_representation(instance)
        # rename all field to camelCase

        response['id'] = response.pop('id')
        response['issuer'] = response.pop('issuer')
        response['title'] = response.pop('title')
        response['description'] = response.pop('description')
        response['contributors'] = response.pop('contributors')
        response['createdAt'] = response.pop('created_at')
        response['updatedAt'] = response.pop('updated_at')
        response['createdBy'] = response.pop('created_by')
        response['updatedBy'] = response.pop('updated_by')

        return response
    
    def create(self, validated_data):
        validated_data['id'] = id_generator(prefix="AWD")

        validated_data['created_by'] = self.context['request'].user.nim
        validated_data['updated_by'] = self.context['request'].user.nim

        return super(AwardSerializer, self).create(validated_data)
    
    def update(self, instance, validated_data):
        validated_data['updated_by'] = self.context['request'].user.nim

        return super(AwardSerializer, self).update(instance, validated_data)
    
