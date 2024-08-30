from datetime import datetime

from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from common import utils
from ..models import User, Role
from ..models_divisions import Division

import copy

from common.utils import id_generator

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

        required_fields = [
            'name',
        ]

        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
            'created_by',
            'updated_by'
        ]

    def create(self, validated_data):

        if self.context['request'].user.is_authenticated:
            validated_data['created_by'] = self.context['request'].user.nim
            validated_data['updated_by'] = self.context['request'].user.nim
        else:
            validated_data['created_by'] = "system"
            validated_data['updated_by'] = "system"

        validated_data['id'] = id_generator(prefix="RLE")

        return super(RoleSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        validated_data['updated_at'] = datetime.now()
        validated_data['updated_by'] = self.context['request'].user.nim

        return super(RoleSerializer, self).update(instance, validated_data)

    def to_representation(self, instance):
        response = super().to_representation(instance)

        response['id'] = response.pop('id', None)
        response['name'] = response.pop('name', None)
        response['createdAt'] = response.pop('created_at', None)
        response['updatedAt'] = response.pop('updated_at', None)
        response['createdBy'] = response.pop('created_by', None)
        response['updatedBy'] = response.pop('updated_by', None)
        

        return response


class DivisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Division
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by', 'updated_by']

    def create(self, validated_data):
        if self.context['request'].user.is_authenticated:
            validated_data['created_by'] = self.context['request'].user.nim
            validated_data['updated_by'] = self.context['request'].user.nim
        else:
            validated_data['created_by'] = "system"
            validated_data['updated_by'] = "system"

        validated_data['id'] = utils.id_generator("DVS")

        return super(DivisionSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        validated_data['updated_at'] = datetime.now()
        validated_data['updated_by'] = self.context['request'].user.nim

        return super(DivisionSerializer, self).update(instance, validated_data)

    def to_representation(self, instance):
        response = super().to_representation(instance)

        response['id'] = response.pop('id', None)
        response['name'] = response.pop('name', None)
        response['description'] = response.pop('description', None)
        response['logoUri'] = response.pop('logo_uri', None)
        response['createdAt'] = response.pop('created_at', None)
        response['updatedAt'] = response.pop('updated_at', None)
        response['createdBy'] = response.pop('created_by', None)
        response['updatedBy'] = response.pop('updated_by', None)

        return response

    def to_internal_value(self, data):
        new_data = copy.deepcopy(data)

        if "logoUri" in data:
            new_data['logo_uri'] = utils.rename_image_file(new_data['logoUri'], prefix="DVS")

        return super().to_internal_value(new_data)

class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer(source="role_id", read_only=True)
    division = DivisionSerializer(source="division_id", read_only=True)
    class Meta:
        model = User
        fields = [
            'nim',
            'name',
            'email',
            'password',
            'role_id',
            'division_id',
            'role',
            'division',
            'major',
            'linkedin_uri',
            'phone_number',
            'profile_uri',
            'year_university_enrolled',
            'period',
            'created_at',
            'updated_at',
            'created_by',
            'updated_by',
            'active',
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
            'period'
        ]

        read_only_fields = [
            'created_at',
            'updated_at',
            'created_by',
            'updated_by',
        ]

    def get_fields(self):
        fields = super(UserSerializer, self).get_fields()

        request = self.context.get('request', None)
        if request and getattr(request, 'method', None) == "PATCH":
            for field in self.Meta.required_fields:
                fields[field].required = False

        return fields

    def to_internal_value(self, data):
        new_data = copy.deepcopy(data)

        if 'roleId' in data:
            new_data['role_id'] = data.get('roleId', None)
        if 'divisionId' in data:
            new_data['division_id'] = data.get('divisionId', None)
        if 'phoneNumber' in data:
            new_data['phone_number'] = data.get('phoneNumber', None)
        if 'profileUri' in data:
            new_data['profile_uri'] = data.get('profileUri', None)
        if 'yearUniversityEnrolled' in data:
            new_data['year_university_enrolled'] = data.get('yearUniversityEnrolled', None)
        if 'yearCommunityEnrolled' in data:
            new_data['period'] = data.get('yearCommunityEnrolled', None)
        if 'linkedinUri' in data:
            new_data['linkedin_uri'] = data.get('linkedinUri', None)
        if 'isActive' in data:
            new_data['active'] = data.get('isActive', None)

        if 'year_university_enrolled' in new_data:
            new_data['year_university_enrolled'] = datetime.strptime(new_data['year_university_enrolled'], '%d-%m-%Y').date()

        if 'period' in new_data:
            new_data['period'] = datetime.strptime(new_data['period'], '%d-%m-%Y').date()


        return super().to_internal_value(new_data)

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))

        if self.context['request'].user.is_authenticated:
            validated_data['created_by'] = self.context['request'].user.nim
            validated_data['updated_by'] = self.context['request'].user.nim
        else:
            validated_data['created_by'] = "system"
            validated_data['updated_by'] = "system"

        role = None
        division = None

        if 'role_id' in validated_data:
            role = Role.objects.filter(id=validated_data['role_id'].id).first()

        if 'division_id' in validated_data:
            division = Division.objects.filter(id=validated_data['division_id'].id).first()

        leader_role = Role.objects.filter(name="Ketua").first()
        sub_leader_role = Role.objects.filter(name="Wakil Ketua").first()

        if division is not None and role is not None:

            if role.id == leader_role.id:
                leader_user = User.objects.filter(role_id=leader_role.id, division_id=division.id).exists()

                if leader_user:
                    raise serializers.ValidationError({
                        "roleId" : ["Leader already exists in this division"]
                    })

            elif role.id == sub_leader_role.id:
                sub_leader_user = User.objects.filter(role_id=sub_leader_role.id, division_id=division.id).exists()

                if sub_leader_user:
                    raise serializers.ValidationError({
                        "roleId" : ["Sub Leader already exists in this division"]
                    })

        return super(UserSerializer, self).create(validated_data)

    def to_representation(self, instance):
        response = super().to_representation(instance)

        response['roleId'] = response.pop('role_id', None)
        response['divisionId'] = response.pop('division_id', None)
        response['role'] = response.pop('role', None)
        response['division'] = response.pop('division', None)
        response['linkedinUri'] = response.pop('linkedin_uri', None)
        response['phoneNumber'] = response.pop('phone_number', None)
        response['profileUri'] = response.pop('profile_uri', None)
        response['yearUniversityEnrolled'] = response.pop('year_university_enrolled', None)
        response['yearCommunityEnrolled'] = response.pop('period', None)
        response['isActive'] = response.pop('active', None)
        response['createdAt'] = response.pop('created_at', None)
        response['updatedAt'] = response.pop('updated_at', None)
        response['createdBy'] = response.pop('created_by', None)
        response['updatedBy'] = response.pop('updated_by', None)

        return response

    def update(self, instance, validated_data):
        validated_data['updated_at'] = datetime.now()
        validated_data['updated_by'] = self.context['request'].user.nim

        update_fields = {
            "role_id": None,
            "division_id": None,
        }

        if 'role_id' in validated_data:
            update_fields['role_id'] = validated_data['role_id']

        if 'division_id' in validated_data:
            update_fields['division_id'] = validated_data['division_id']

        if update_fields['role_id'] is None and update_fields['division_id'] is None:
            return super(UserSerializer, self).update(instance, validated_data)

        if update_fields['role_id'] is None:
            if instance.role_id is not None:
                update_fields['role_id'] = instance.role_id

        if update_fields['division_id'] is None:
            if instance.division_id is not None:
                update_fields['division_id'] = instance.division_id

        if update_fields['division_id'] is None or update_fields['role_id'] is None:
            return super(UserSerializer, self).update(instance, validated_data)

        role_leader = Role.objects.filter(name='Ketua')
        role_sub_leader = Role.objects.filter(name='Wakil Ketua')

        if not role_leader.exists() or not role_sub_leader.exists():
            return super(UserSerializer, self).update(instance, validated_data)

        if update_fields['role_id'].id != role_leader.first().id and update_fields['role_id'].id != role_sub_leader.first().id:
            return super(UserSerializer, self).update(instance, validated_data)


        if update_fields['division_id'].id == role_leader.first().id:
            leader_user = User.objects.filter(role_id=role_leader.first().id,
                                              division_id=update_fields['division_id'].id).exclude(nim=instance.nim).exists()

            if leader_user:
                raise serializers.ValidationError({
                    "roleId" : ["Leader already exists in this division"]
                })

        elif update_fields['division_id'].id == role_sub_leader.first().id:
            sub_leader_user = User.objects.filter(role_id=role_sub_leader.first().id,
                                                  division_id=update_fields['division_id'].id).exclude(nim=instance.nim).exists()

            if sub_leader_user:
                raise serializers.ValidationError({
                    "roleId" : ["Sub Leader already exists in this division"]
                })

        return super(UserSerializer, self).update(instance, validated_data)

    def delete(self, instance):
        instance.active = False
        instance.save()

        return instance

    def get_role(self, obj):
        return obj.role_id

    def get_division(self, obj):
        return obj.division_id


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