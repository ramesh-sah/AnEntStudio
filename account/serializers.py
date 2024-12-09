from rest_framework import serializers
from account.models import User,UserOTP
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from django.contrib.auth import get_user_model


# from account.utils import Util



domain = "https://gms.anitaricemill.com"

# class UserSerializer(serializers.ModelSerializer):
#     avatar_url = serializers.SerializerMethodField('get_image_url')

#     class Meta:
#         model = User
#         fields = ['id', 'name','email','password','phone_No','avatar','avatar_url','is_admin','is_user']

#     def get_image_url(self, obj):
#         if obj.avatar:
#             return f'{domain}{obj.avatar.url}'


from rest_framework import serializers
from .models import User, UserOTP

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email', 'name', 'phone_No', 'password']
        read_only_fields = ['id']  # Specify user_id as a read-only field
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        otp_instance = UserOTP(user=user)
        otp_instance.generate_otp()
        otp_instance.send_otp()
        return user

class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserOTP
        fields = ['otp_code']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    
    class Meta:
        model = User
        fields=['id','email', 'name', 'password', 'password2', 'phone_No']
        read_only_fields = ['id']  # Specify user_id as a read-only field
        extra_kwargs={
        'password':{'write_only':True}
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password don't match !")
        return attrs

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email', 'password']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name','phone_No','avatar']


class UserChangePasswordSerializer(serializers.Serializer):
    oldPassword = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    newPassword = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    confirmPassword = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    class Meta:
        fields = ['oldPassword', 'newPassword','confirmPassword']
        




import random
import datetime
from django.utils import timezone
class SendPasswordResetEmailSerializer(serializers.Serializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    fields = ['email']

  def validate(self, attrs):
    email = attrs.get('email')
    if User.objects.filter(email=email).exists():
      user = User.objects.get(email = email)
      uid = urlsafe_base64_encode(force_bytes(user.id))

      otp_code = str(random.randint(1000, 9999))

      expiration_time = timezone.now() + datetime.timedelta(minutes=5)

      userotp =UserOTP.objects.filter(user=user).first()
      print("OTP Code:",otp_code)
      print(timezone.now())
      print("Expired time:",expiration_time)
      print(userotp)
      if userotp:
        userotp.otp_code = otp_code
        userotp.otp_code_expiration = expiration_time
        userotp.save()
      else:
         userotp = UserOTP.objects.create(user=user,otp_code = otp_code,otp_code_expiration = expiration_time)

      # Send the email with the OTP
      body = f'Your OTP code for password reset is: {otp_code}'
      data = {
          'subject': 'Reset Your Password',
          'body': body,
          'to_email': user.email
      }

      # Send email using your Util class
      Util.send_email(data)

      return attrs
    else:
      raise serializers.ValidationError('You are not a Registered User')




# otp validatin serializer
class OTPValidationSerializer(serializers.Serializer):

    otp_code = serializers.CharField(max_length=150, style={'type': 'number'}, write_only=True)

    class Meta:
        fields = ['otp_code']

    def validate(self, attrs):
        try:
            otp_code = attrs.get('otp_code')
            otp_details = UserOTP.objects.get(otp_code=otp_code)
            userotp = UserOTP.objects.get(user=otp_details.user.id)

            if userotp.otp_code != otp_code:
                raise serializers.ValidationError('Invalid OTP code')

            if userotp.otp_code_expiration is not None and userotp.otp_code_expiration < timezone.now():
                raise serializers.ValidationError('OTP code has expired')

            attrs['user'] = otp_details.user 
            return attrs
        except UserOTP.DoesNotExist:
            raise serializers.ValidationError('Invalid OTP code')
        except Exception as e:
            raise serializers.ValidationError('Failed to validate OTP code')



class UserPasswordResetSerializer(serializers.Serializer):
    newPassword = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    confirmPassword = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    class Meta:
        fields = ['newPassword', 'confirmPassword']

    def validate(self, attrs):
        try:
            password = attrs.get('newPassword')
            confirmPassword = attrs.get('confirmPassword')
            user = self.context.get('user')
            print(user)
            userotp = UserOTP.objects.get(user=user)

            if password != confirmPassword:
                raise serializers.ValidationError("Password and Confirm Password don't match")


            if userotp.otp_code_expiration is not None and userotp.otp_code_expiration < timezone.now():
                raise serializers.ValidationError('OTP code has expired')

            user.set_password(password)
            user.set_password(confirmPassword)
            user.save()

            return attrs
        except Exception as e:
            print(e)
            raise serializers.ValidationError('Failed to reset the password')



from typing import Optional, Type, Dict, Any
from rest_framework import serializers
from rest_framework_simplejwt.tokens import Token, RefreshToken, SlidingToken
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.settings import api_settings
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

### Access token for refresh

class TokenObtainSerializer(serializers.Serializer):
    username_field = get_user_model().USERNAME_FIELD
    token_class: Optional[Type[Token]] = None

    default_error_messages = {
        "no_active_account": _("No active account found with the given credentials")
    }

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.CharField(write_only=True)
        self.fields["password"] = serializers.CharField(write_only=True)

    def validate(self, attrs: Dict[str, Any]) -> Dict[Any, Any]:
        # Check if the expected field is present in the attrs
        if self.username_field not in attrs:
            raise serializers.ValidationError({self.username_field: f"{self.username_field} is required."})

        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            "password": attrs["password"],
        }
        try:
            authenticate_kwargs["request"] = self.context["request"]
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)

        if not api_settings.USER_AUTHENTICATION_RULE(self.user):
            raise serializers.ValidationError(
                self.error_messages["no_active_account"],
                "no_active_account",
            )

        return {}


    @classmethod
    def get_token(cls, user: get_user_model()) -> Token:
        return cls.token_class.for_user(user)  # type: ignore



class TokenObtainPairSerializer(TokenObtainSerializer):
    token_class = RefreshToken

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


class TokenObtainSlidingSerializer(TokenObtainSerializer):
    token_class = SlidingToken

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        data = super().validate(attrs)

        token = self.get_token(self.user)

        data["token"] = str(token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


class TokenRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField(read_only=True)
    token_class = RefreshToken

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        refresh = self.token_class(attrs["refresh"])

        data = {"access": str(refresh.access_token)}

        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    # Attempt to blacklist the given refresh token
                    refresh.blacklist()
                except AttributeError:
                    # If blacklist app not installed, blacklist method will
                    # not be present
                    pass

            refresh.set_jti()
            refresh.set_exp()
            refresh.set_iat()

            data["refresh"] = str(refresh)

        return data


class TokenRefreshSlidingSerializer(serializers.Serializer):
    token = serializers.CharField()
    token_class = SlidingToken

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        token = self.token_class(attrs["token"])

        # Check that the timestamp in the "refresh_exp" claim has not
        # passed
        token.check_exp(api_settings.SLIDING_TOKEN_REFRESH_EXP_CLAIM)

        # Update the "exp" and "iat" claims
        token.set_exp()
        token.set_iat()

        return {"token": str(token)}


class TokenVerifySerializer(serializers.Serializer):
    token = serializers.CharField(write_only=True)

    def validate(self, attrs: Dict[str, None]) -> Dict[Any, Any]:
        token = UntypedToken(attrs["token"])

        if (
            api_settings.BLACKLIST_AFTER_ROTATION
            and "rest_framework_simplejwt.token_blacklist" in settings.INSTALLED_APPS
        ):
            jti = token.get(api_settings.JTI_CLAIM)
            if BlacklistedToken.objects.filter(token__jti=jti).exists():
                raise ValidationError("Token is blacklisted")

        return {}


class TokenBlacklistSerializer(serializers.Serializer):
    refresh = serializers.CharField(write_only=True)
    token_class = RefreshToken

    def validate(self, attrs: Dict[str, Any]) -> Dict[Any, Any]:
        refresh = self.token_class(attrs["refresh"])
        try:
            refresh.blacklist()
        except AttributeError:
            pass
        return {}
