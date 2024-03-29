from rest_framework import serializers


class ValidationErrorSerializer(serializers.Serializer):
    name = serializers.CharField(allow_null=True)
    message = serializers.CharField(allow_null=True)



class GenericErrorSerializer(serializers.Serializer):
    name = serializers.CharField(allow_null=True)
    message = serializers.CharField(allow_null=True)
    validation = ValidationErrorSerializer(allow_null=True, many=True)


class ResponseSerializer(serializers.Serializer):
    code = serializers.IntegerField()
    status = serializers.CharField()
    recordsTotal = serializers.IntegerField()
    data = serializers.SerializerMethodField()
    error = GenericErrorSerializer(allow_null=True)

    def get_data(self, instance):
        data = instance.get('data')

        return data
