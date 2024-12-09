from django.shortcuts import render, redirect
from rest_framework.response import Response
from django.contrib.auth import login,logout
from rest_framework import status
from rest_framework.views import APIView

from account.serializers import  (UserLoginSerializer, 
                                    UserRegistrationSerializer,
                                    UserProfileSerializer,
                                    UserChangePasswordSerializer,
                                    SendPasswordResetEmailSerializer,
                                    UserPasswordResetSerializer,
                                    UserSerializer,
                                   
                                )
from django.contrib.auth import authenticate
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from . models import User,UserOTP
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework import generics
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenViewBase
from account.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
    TokenVerifySerializer,
    TokenBlacklistSerializer
)



# Generate Token Manually
@csrf_exempt
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }

class UserRegistrationView(APIView):
  #renderer_classes = [UserRenderer]
  def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        
        # Validate the incoming data
        serializer.is_valid(raise_exception=True)
        
        # Check if the user already exists (based on email or phone number)
        user_exists = User.objects.filter(email=request.data.get('email')).exists() or \
                    User.objects.filter(phone_No=request.data.get('phone_No')).exists()

        if user_exists:
            return Response({
                'message': 'User with this email or phone number already exists.',
                'success': 'false'
            }, status=status.HTTP_400_BAD_REQUEST)

        # If user does not exist, save the new user
        user = serializer.save()
        token = get_tokens_for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'token': token,
            'message': 'Register Successful!',
            'success': 'true',
        }, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
#   renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    password = serializer.data.get('password')
    if User.objects.filter(email =email):
        user = authenticate(email=email, password=password)
        if user is not None:
            token = get_tokens_for_user(user)
            login(request, user)
            return Response({'user':UserSerializer(user).data,'token':token, 'message':'Login Successfully !', 'success':'true'}, status=status.HTTP_200_OK)
        else:
            return Response({'message':'Password Invalid !','success':'false'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'message':'User does not exists!', 'success':'false'}, status=status.HTTP_400_BAD_REQUEST)
      

class UserProfileView(APIView):
  # renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def get(self, request, format=None):
    serializer = UserProfileSerializer(request.user)
    return Response({'user':UserSerializer(request.user).data,'message':'User get successfully', 'success':'true'}, status=status.HTTP_200_OK)



  def put(self, request, formate = None):
    profile = request.user
    serializer = UserProfileSerializer(profile, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'user':UserSerializer(request.user).data,'message':'Update  successfully !', 'success':'true'}, status=status.HTTP_200_OK)




class UserChangePasswordView(APIView):
  # renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def post(self, request, format=None):
    serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
    serializer.is_valid(raise_exception=True)
    oldpassword = serializer.validated_data['oldPassword']
    password = serializer.validated_data['newPassword']
    password2 = serializer.validated_data['confirmPassword']
    user = request.user
    if user.check_password(oldpassword):
      if password != password2:
        return Response({'message':"Password doesn't match !",'success':'false'}, status = status.HTTP_400_BAD_REQUEST)
      user.set_password(password)
      user.save()
      return Response({'message':'Password Change Successfully !','success':'true'}, status=status.HTTP_200_OK)
    return Response({'message':"Old Password does not match !",'success':'false'}, status=status.HTTP_400_BAD_REQUEST)

  
class SendPasswordResetEmailView(APIView):
  # renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = SendPasswordResetEmailSerializer(data=request.data)
    print(request.data)
    serializer.is_valid(raise_exception=True)
    return Response({'message':'Verify your email !', 'success':'true'}, status=status.HTTP_200_OK)



# class OTPValidation(APIView):
#   def post(self, request, format= None):
#       serializer = OTPValidationSerializer(data=request.data)
#       if serializer.is_valid():
#           user = serializer.validated_data['user']
#           response_data = {'message': 'OTP code validated successfully!', 'success': True, 'user_id': user.id}
#           return Response(response_data, status=status.HTTP_200_OK)

#       else:
#           return Response({'message': 'OTP code validation failed!', 'success': False}, status=status.HTTP_400_BAD_REQUEST)

from django.utils import timezone
class UserPasswordResetView(APIView):
    def post(self, request, format=None):
        user_id = request.data.get('user_id')  
        user = User.objects.get(id=user_id)
        password_reset_serializer = UserPasswordResetSerializer(data=request.data, context={'user': user})
        
        if password_reset_serializer.is_valid():
            new_password = password_reset_serializer.validated_data['newPassword']
            confirm_password = password_reset_serializer.validated_data['confirmPassword']

            if new_password != confirm_password:
                return Response({'message': 'New password and confirm password do not match.', 'success': False}, status=status.HTTP_400_BAD_REQUEST)

            userotp = UserOTP.objects.get(user=user)
            if userotp.otp_code_expiration is not None and userotp.otp_code_expiration < timezone.now():
                return Response({'message': 'OTP code has expired.', 'success': False}, status=status.HTTP_400_BAD_REQUEST)

            # Reset the password for the user
            user.set_password(new_password)
            user.save()

            return Response({'message': 'Password reset successfully!', 'success': True}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Failed to reset the password!', 'success': False}, status=status.HTTP_400_BAD_REQUEST)
        
        
class VerifyOTPView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        otp_code = request.data.get('otp_code')

        try:
            user_otp = UserOTP.objects.get(user_id=user_id)

            if timezone.now() > user_otp.otp_code_expiration:
                return Response({"error": "OTP expired. Please resend."}, status=status.HTTP_400_BAD_REQUEST)

            if user_otp.otp_code == otp_code:
                # OTP verified successfully
                return Response({"message": "OTP verified successfully!"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid OTP. Please try again."}, status=status.HTTP_400_BAD_REQUEST)

        except UserOTP.DoesNotExist:
            return Response({"error": "User OTP not found."}, status=status.HTTP_404_NOT_FOUND)

class ResendOTPView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')

        try:
            user_otp = UserOTP.objects.get(user_id=user_id)
            user_otp.generate_otp()
            user_otp.send_otp()
            return Response({"message": "OTP resent successfully!"}, status=status.HTTP_200_OK)

        except UserOTP.DoesNotExist:
            return Response({"error": "User OTP not found."}, status=status.HTTP_404_NOT_FOUND)





# logout User
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        print("Received refresh token:", refresh_token)

        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
                print("Successfully logged out.")
                return Response({"detail": "Successfully logged out."})
            except Exception as e:
                print("Error during logout:", e)
                return Response({"detail": "Invalid token or token expired."}, status=400)
        else:
            print("Refresh token not provided.")
            return Response({"detail": "Refresh token not provided."}, status=400)


# View for obtaining token pair (access and refresh tokens)
class TokenObtainPairView(TokenViewBase):
    serializer_class = TokenObtainPairSerializer


# View for refreshing the access token using a refresh token
class TokenRefreshView(TokenViewBase):
    serializer_class = TokenRefreshSerializer


# View for verifying the token validity
class TokenVerifyView(generics.GenericAPIView):
    serializer_class = TokenVerifySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(status=status.HTTP_200_OK)


# View for blacklisting (revoking) the refresh token
class TokenBlacklistView(generics.GenericAPIView):
    serializer_class = TokenBlacklistSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(status=status.HTTP_205_RESET_CONTENT)