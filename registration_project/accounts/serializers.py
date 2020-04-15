from django.contrib.auth import get_user_model
from rest_framework import serializers



User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    password        = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password2       = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'password2',
        ]
        extra_kwargs = {'password':{'write_only':True}}
        required_fields = fields

class UserLoginSerializer(serializers.ModelSerializer):
    password        = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = User
        fields = [
            'username',
            'password',
        ]
        extra_kwargs = {'password':{'write_only':True}}

class ResetPasswordSerializer(serializers.ModelSerializer):
    new_password        = serializers.CharField(style={'input_type': 'password'}, write_only=True, required=True)
    new_password_confirm       = serializers.CharField(style={'input_type': 'password'}, write_only=True, required=True)
    class Meta:
        model = User
        fields = [
            'new_password',
            'new_password_confirm',
        ]
        required_fields = fields