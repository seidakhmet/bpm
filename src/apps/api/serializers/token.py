from rest_framework import serializers


class TokenRequestSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(required=True)
    data = serializers.CharField(required=True)


class TokenResponseSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
