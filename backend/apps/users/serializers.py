from rest_framework import serializers

from .models import CustomUser

class PublicCustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'public_field')