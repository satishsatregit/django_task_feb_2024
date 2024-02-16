# serializers.py
from rest_framework import serializers
from .models import CustomUser,Content_item

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content_item
        fields = '__all__'
