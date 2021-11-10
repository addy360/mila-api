from rest_framework import serializers


class ContactSerializer(serializers.Serializer):
    fullname = serializers.CharField(max_length=50)
    email = serializers.EmailField()
    message = serializers.CharField()
