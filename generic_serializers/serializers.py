from rest_framework import serializers

from users.models import User
from users.v1.serializers import UserProfileSerializer


class ResponseSerializer(serializers.Serializer):
    code = serializers.IntegerField()
    status = serializers.CharField()
    recordsTotal = serializers.IntegerField()
    data = serializers.SerializerMethodField()
    error = serializers.CharField(allow_null=True)

    def get_data(self, instance):
        data = instance.get('data')

        return data
