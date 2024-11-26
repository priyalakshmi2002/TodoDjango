from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Todo

class SignupSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    email = serializers.EmailField(required=True) 

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with that username already exists")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists")
        return value

    def validate(self, data):
        password1 = data.get('password1')
        password2 = data.get('password2')
        if password1 != password2:
            raise serializers.ValidationError({'password2': "Passwords do not match"})
        if len(password1) < 6:
            raise serializers.ValidationError({'password1': "Password must be at least 6 characters long"})
        return data

    def create(self, validated_data):
        validated_data.pop('password2') 
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password1']
        )
        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        error_messages={'blank': 'Username is required.'}
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        error_messages={'blank': 'Password is required.'}
    )

    def validate(self, data):
        return data

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['id', 'user', 'title', 'description','assigned_to', 'completed']

