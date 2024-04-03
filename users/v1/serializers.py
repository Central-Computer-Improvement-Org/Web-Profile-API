from datetime import datetime

from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from ..models import User, Role
from ..models_divisions import Division


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'nim',
            'name',
            'email',
            'password',
            'role_id',
            'division_id',
            'major',
            'linkedin_uri',
            'phone_number',
            'profile_uri',
            'year_university_enrolled',
            'year_community_enrolled',
            'created_at',
            'updated_at',
            'created_by',
            'updated_by'
        ]

        extra_kwargs = {
            'password': {
                'write_only': True
            },
        }

        required_fields = [
            'nim',
            'name',
            'email',
            'password',
            'role_id',
            'phone_number',
            'profile_uri',
            'year_university_enrolled',
            'year_community_enrolled'
        ]

        read_only_fields = [
            'created_at',
            'updated_at',
            'created_by',
            'updated_by'
        ]

    def to_internal_value(self, data):
        if 'roleId' in data:
            data['role_id'] = data.get('roleId', None)
        if 'divisionId' in data:
            data['division_id'] = data.get('divisionId', None)
        if 'phoneNumber' in data:
            data['phone_number'] = data.get('phoneNumber', None)
        if 'profileUri' in data:
            data['profile_uri'] = data.get('profileUri', None)
        if 'yearUniversityEnrolled' in data:
            data['year_university_enrolled'] = data.get('yearUniversityEnrolled', None)
        if 'yearCommunityEnrolled' in data:
            data['year_community_enrolled'] = data.get('yearCommunityEnrolled', None)
        if 'linkedinUri' in data:
            data['linkedin_uri'] = data.get('linkedinUri', None)

        if data['year_university_enrolled']:
            data['year_university_enrolled'] = datetime.strptime(data['year_university_enrolled'], '%d-%m-%Y').date()

        if data['year_community_enrolled']:
            data['year_community_enrolled'] = datetime.strptime(data['year_community_enrolled'], '%d-%m-%Y').date()

        return super().to_internal_value(data)

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))

        if self.context['request'].user.is_authenticated:
            validated_data['created_by'] = self.context['request'].user.nim
            validated_data['updated_by'] = self.context['request'].user.nim
        else:
            validated_data['created_by'] = "system"
            validated_data['updated_by'] = "system"

        return super(UserSerializer, self).create(validated_data)

    def to_representation(self, instance):
        response = super().to_representation(instance)

        response['roleId'] = response.pop('role_id', None)
        response['divisionId'] = response.pop('division_id', None)
        response['linkedinUri'] = response.pop('linkedin_uri', None)
        response['phoneNumber'] = response.pop('phone_number', None)
        response['profileUri'] = response.pop('profile_uri', None)
        response['yearUniversityEnrolled'] = response.pop('year_university_enrolled', None)
        response['yearCommunityEnrolled'] = response.pop('year_community_enrolled', None)
        response['createdAt'] = response.pop('created_at', None)
        response['updatedAt'] = response.pop('updated_at', None)
        response['createdBy'] = response.pop('created_by', None)
        response['updatedBy'] = response.pop('updated_by', None)

        return response


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nim', 'name', 'email', 'role_id', 'division_id', 'phone_number', 'profile_uri']

    def to_representation(self, instance):
        response = super().to_representation(instance)

        response['roleId'] = response.pop('role_id')
        response['divisionId'] = response.pop('division_id')
        response['phoneNumber'] = response.pop('phone_number')
        response['profileUri'] = response.pop('profile_uri')

        return response


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class DivisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Division
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']

    def create(self, validated_data):
        if self.context['request'].user.is_authenticated:
            validated_data['created_by'] = self.context['request'].user.nim
            validated_data['updated_by'] = self.context['request'].user.nim
        else:
            validated_data['created_by'] = "system"
            validated_data['updated_by'] = "system"

        return super(DivisionSerializer, self).create(validated_data)
