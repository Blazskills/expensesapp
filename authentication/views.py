from django.shortcuts import render
from rest_framework import generics, status, views
from rest_framework.exceptions import AuthenticationFailed
from .serializers import EmailVerificationSerializer, RegisterSerializer, LoginSerializer, ResetPasswordEmailRequestSerializer, SetNewPasswordSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import Util
from .models import User
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
import jwt
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .renderers import UserRenderer
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
import smtplib
from django.contrib import auth
from smtplib import SMTPException
# Create your views here.


class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer

    renderer_class = (UserRenderer,)

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        print(user)
        token = RefreshToken.for_user(user).access_token
        # print(token)
        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')
        absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
        message = 'Hi ' + user.username + \
            ' Use link to verify your email, it expires in 5min \n' + absurl
        email_from = settings.EMAIL_HOST_USER
        email_to = user.email
        data = {
            'subject': 'Verify your email', 'message': message, 'email_from': email_from, 'email_to': email_to
        }
        try:
            Util.send_email(data)
        except:
            unsucessfully_registered_email = user.id
            # print(unsucessfully_registered_email)
            User.objects.filter(id=unsucessfully_registered_email).delete()
            # print(unsucessfully_registered_email)
            return Response({'error': 'something went wrong with your email. Kindly specify correct and validated email address. Note, this email is not accepted and has been deleted'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer
    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms="HS256")
            user = User.objects.get(id=payload['user_id'])
            print(payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
                return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
            return Response({'email': 'Account verified.'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        email = request.data['email']
        password = request.data['password']
        user = auth.authenticate(email=email, password=password)
        if user:  
            # user = User.objects.get(email=email)
            if not user.is_verified:
                if user.is_active:
                    token = RefreshToken.for_user(user).access_token
                    current_site = get_current_site(request).domain
                    relativeLink = reverse('email-verify')
                    absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
                    message = 'Hi ' + user.username + \
                        ' Use link to verify your email, it expires in 5min \n' + absurl
                    email_from = settings.EMAIL_HOST_USER
                    email_to = user.email
                    data = {
                            'subject': 'Verify your email', 'message': message, 'email_from': email_from, 'email_to': email_to
                        }
                    try:
                        Util.send_email(data)
                        return Response({'succes': 'Account not verified. Kindly check your email to verifiy your account.'}, status=status.HTTP_200_OK)
                    except SMTPException as e:
                        return Response({'error': (f"There was an error sending an email.Something went wrong with your email.{e}")}, status=status.HTTP_406_NOT_ACCEPTABLE)
                    except:                  
                        return Response({'error': 'Mail Sending Failed!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
                raise AuthenticationFailed('Account disable, Contact admin.')
            data_verified= {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens()
            }
            return Response(data_verified, status=status.HTTP_200_OK)
        raise AuthenticationFailed('Invalid Credentials, Try again')
        # print(user)
        # print(token)

        # serializer.is_valid(raise_exception=True)
        # datas =  {
        #     'email': user.email,
        #     'username': user.username,
        #     'tokens': user.tokens()
        # }
        # return Response(datas, status=status.HTTP_200_OK)



# Stage 1 of reset password. This method takes the email alone and send it to the user. If user email is not valid or valid, it will still send the reset password to the email provided.
class RequestPasswordRestEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        email = request.data['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            relativeLink = reverse(
                'password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
            absurl = 'http://'+current_site + relativeLink
            message = 'Hello, \n Use link to reset your password here \n' + absurl
            email_from = settings.EMAIL_HOST_USER
            email_to = user.email
            data = {
                'subject': 'Reset your password', 'message': message, 'email_from': email_from, 'email_to': email_to
            }
            try:
                Util.send_email(data)

            except smtplib.SMTPRecipientsRefused:
                return Response(f'server rejected recepients. Email can not be used,kindly provide another email',
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'success': 'We have sent you a reset password link to your email address'},  status=status.HTTP_200_OK)

# Stage 2 Reset method password, this method decode and check the reset password tokens is valid. Note: major part of the reset password method
class PasswordTokenCheckApi(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer
    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token not valid any more, kindly request for a new password reset token'},  status=status.HTTP_401_UNAUTHORIZED)
            return Response({'success': True, 'message': 'Credentials valid', 'uidb64': uidb64, 'token': token}, status=status.HTTP_200_OK)
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user)
            return Response({'error': 'Token not valid any more or has been tampered with, kindly request for a new password reset token'},  status=status.HTTP_401_UNAUTHORIZED)

#Stage 3 Reset method password, this method allows users to input new password and update the old password with the new password provided by the user.
class SetNewPasswordApiView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'New password reset successfully'}, status=status.HTTP_200_OK)


# class VerifyEmail(views.APIView):
#     serializer_class = EmailVerificationSerializer
#     token_param_config = openapi.Parameter(
#         'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

#     @swagger_auto_schema(manual_parameters=[token_param_config])
#     def get(self, request):
#         token = request.GET.get('token')
#         try:
#             payload = jwt.decode(token, settings.SECRET_KEY)
#             print(payload)
#             user = User.objects.get(id=payload['user_id'])
#             print(user)
#             if not user.is_verified:
#                 user.is_verified = True
#                 user.save()
#             return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
#         except jwt.ExpiredSignatureError as identifier:
#             return Response({'error': 'Activation Link Expired'}, status=status.HTTP_400_BAD_REQUEST)
#         except jwt.exceptions.DecodeError as identifier:
#             return Response({'error': 'Invalid token, Request new token'}, status=status.HTTP_400_BAD_REQUEST)
