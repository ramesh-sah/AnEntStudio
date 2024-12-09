from django.urls import path
from account.views import (UserLoginView,
                            UserRegistrationView,
                            UserProfileView,
                            UserChangePasswordView,
                            SendPasswordResetEmailView,
                            UserPasswordResetView,
                            LogoutView,VerifyOTPView, ResendOTPView,

                            TokenObtainPairView,
                            TokenRefreshView,
                            TokenVerifyView,
                            TokenBlacklistView
                            )                       
urlpatterns = [
    path('register', UserRegistrationView.as_view(), name='register'),
    path('login', UserLoginView.as_view(), name='login'),
    path('profile', UserProfileView.as_view(), name='profile'),
    path('update/profile', UserProfileView.as_view(), name='profile'),
    path('change/password', UserChangePasswordView.as_view(), name='changepassword'),
    path('forgot/password', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
     path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('resend-otp/', ResendOTPView.as_view(), name='resend_otp'),
    path('reset/password', UserPasswordResetView.as_view(), name='reset-password'),
    path('logout', LogoutView.as_view(), name='logout'),

    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),

]