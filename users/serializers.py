from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']

class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class UserRegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=255, write_only=True)
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'password', 'confirm_password']
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'password': {'write_only': True},
        }
    def validate(self, data):
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError({"confirm_password": ["The passwords does not match."]})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        return User.objects.create_user(**validated_data)