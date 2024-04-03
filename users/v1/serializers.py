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
        ]
        extra_kwargs = {
            'password': {
                'write_only': True
            },
        }

    def to_internal_value(self, data):
        data['role_id'] = data.get('roleId', None)
        data['division_id'] = data.get('divisionId', None)
        data['phone_number'] = data.get('phoneNumber', None)
        data['profile_uri'] = data.get('profileUri', None)
        data['year_university_enrolled'] = data.get('yearUniversityEnrolled', None)
        data['year_community_enrolled'] = data.get('yearCommunityEnrolled', None)
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

        response['roleId'] = response.pop('role_id')
        response['divisionId'] = response.pop('division_id')
        response['linkedinUri'] = response.pop('linkedin_uri')
        response['phoneNumber'] = response.pop('phone_number')
        response['profileUri'] = response.pop('profile_uri')
        response['yearUniversityEnrolled'] = response.pop('year_university_enrolled')
        response['yearCommunityEnrolled'] = response.pop('year_community_enrolled')

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

    def create(self, validated_data):
        if self.context['request'].user.is_authenticated:
            validated_data['created_by'] = self.context['request'].user.nim
            validated_data['updated_by'] = self.context['request'].user.nim
        else:
            validated_data['created_by'] = "system"
            validated_data['updated_by'] = "system"

        return super(DivisionSerializer, self).create(validated_data)
