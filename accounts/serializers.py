from rest_framework import serializers
from rest_framework.validators import ValidationError
from django.contrib.auth.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password']

    def validate(self, attrs):
        # Custom validation for the serializer fields
        username = attrs['username']

        # Check if the email already exists
        email_exists = User.objects.filter(email=attrs['email']).exists()
        if email_exists:    
            raise ValidationError("Email already exists!")
        
        # Check if the username already exists
        username_exists = User.objects.filter(username=username).exists()
        if username_exists:    
            raise ValidationError("Username already exists!")
    
        # Check if the username length is greater than four characters
        if len(username) < 4:
            raise ValidationError('Username must be greater than four characters')
        
        # Check if the username is a numeric value
        if username.isdigit():
            raise ValidationError('Username must not be a numeric value')
        
        return super().validate(attrs)
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password) # Hash the password
        user.save()
        return user
        

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=80)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        fields = ["email", "password"]