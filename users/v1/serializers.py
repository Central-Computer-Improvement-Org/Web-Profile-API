from rest_framework import serializers

from ..models import User, Role


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {
                'write_only': True
            },
        }


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nim', 'name', 'email', 'role_id', 'division_id', 'phone_number', 'profile_uri']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        # rename all field to camelCase

        response['roleId'] = response.pop('role_id')
        response['divisionId'] = response.pop('division_id')
        response['phoneNumber'] = response.pop('phone_number')
        response['profileUri'] = response.pop('profile_uri')

        return response


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'
