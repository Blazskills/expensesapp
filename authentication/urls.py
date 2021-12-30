from django.urls import path
from .views import LoginAPIView, LogoutApiView, PasswordTokenCheckApi, RegisterView, RequestPasswordRestEmail, SetNewPasswordApiView, VerifyEmail
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
    path('login/', LoginAPIView.as_view(), name="login"),
    path('logout/', LogoutApiView.as_view(), name="logout"),
    # reset password stage 1
    path('request-reset-email/', RequestPasswordRestEmail.as_view(),
         name="request-reset-email"),
    # Reset password stage 2
    path('password-reset/<uidb64>/<token>/',
         PasswordTokenCheckApi.as_view(), name="password-reset-confirm"),
    # Reset password stage 3
    path('password-reset-complete/', SetNewPasswordApiView.as_view(), name="password-reset-complete"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),



]
