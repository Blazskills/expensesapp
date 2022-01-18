from django.contrib.sites.shortcuts import get_current_site
from django.db.models import fields
from django.conf import settings
from django.urls import reverse
from rest_framework import serializers
from .models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .utils import Util
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'first_name', 'last_name']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError(
                'The username should only contain alphanumeric characters')

        if len(username) < 3:
            raise serializers.ValidationError(
                'The username should be greater than 2')
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']


class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    first_name = serializers.CharField(
        max_length=255, min_length=3, read_only=True)
    last_name = serializers.CharField(
        max_length=68, min_length=6, read_only=True)
    username = serializers.CharField(
        max_length=255, min_length=3, read_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])
        return {
            'access': user.tokens()['access'],
            'refresh': user.tokens()['refresh']
        }

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email',
                  'password', 'username', 'tokens']

    # def validate(self, attrs):
    #     email = attrs.get('email', '')
    #     password = attrs.get('password', '')

    #     user = auth.authenticate(email=email, password=password)

    #     if not user:
    #         raise AuthenticationFailed('Invalid Credentials, Try again')
    #     if not user.is_active:
    #         raise AuthenticationFailed('Account disable, Contact admin.')
    #     if not user.is_verified:
    #         raise AuthenticationFailed('Email is not verified.')

        # return {
        #     'email': user.email,
        #     'username': user.username,
        #     'tokens': user.tokens()
        # }
        # return super().validate(attrs)


# serializer for Stage 1 of reset password. This method takes the email alone and send it to the user. If user email is not valid or valid, it will still send the reset password to the email provided.
class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)
    redirect_url = serializers.CharField(max_length=255, required=False)

    class Meta:
        fields = ['email']


# Stage 3 Reset method password, this method allows users to input new password and update the old password with the new password provided by the user.
class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')
            id = (urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):  # This check if token has been used or not
                raise AuthenticationFailed(
                    'The reset link is invalid. Might have been used already', 401)
            user.set_password(password)
            user.save()
            return user
        except Exception as e:
            # Unable to validate the tokens or uidb64
            raise AuthenticationFailed('The reset link is invalid', 401)

        return super().validate(attrs)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': ('Token expired or Invalid token'),
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError as e:
            self.fail('bad_token')
