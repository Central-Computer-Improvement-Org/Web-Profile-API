from rest_framework import serializers


class DataSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return instance


class ResponseSerializer(serializers.Serializer):
    code = serializers.IntegerField()
    status = serializers.CharField()
    recordsTotal = serializers.IntegerField()
    data = DataSerializer(many=True)
    error = serializers.CharField(allow_null=True)
