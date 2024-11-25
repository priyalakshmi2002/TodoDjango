from rest_framework import serializers
from django.contrib.auth.models import User

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

        # Check if passwords match
        if password1 != password2:
            raise serializers.ValidationError({'password2': "Passwords do not match"})

        # Check password strength (example: minimum length)
        if len(password1) < 6:
            raise serializers.ValidationError({'password1': "Password must be at least 6 characters long"})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')  # Remove password2 since it's not a field in the User model
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password1']
        )
        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        # If username or password is missing
        if not username or not password:
            raise serializers.ValidationError("Both fields are required.")
        return data

