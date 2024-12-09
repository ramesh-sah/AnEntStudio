from datetime import timezone
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.apps import apps
import  requests
import random

#  Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, name, phone_No, password=None, password2=None):
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            phone_No=phone_No
        )

        user.set_password(password)
        user.is_user = True 
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, phone_No, password=None):
        user = self.create_user(
            email,
            password=password,
            name=name, 
            phone_No=phone_No
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

#  Custom User Model
class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=200)
    is_user = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    phone_No = models.CharField(max_length=150)
    avatar = models.ImageField(upload_to="avatarimage/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone_No']

    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


# OTP Model
class UserOTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_otp')
    otp_code = models.CharField(max_length=4)
    otp_code_expiration = models.DateTimeField()

    def __str__(self):
        return f"{self.user.name} - {self.otp_code}"

    def generate_otp(self):
        self.otp_code = str(random.randint(1000, 9999))
        self.otp_code_expiration = timezone.now() + timezone.timedelta(minutes=5)
        self.save()

    def send_otp(self):
        """Sends the OTP to the user's mobile number."""
        auth_token = '<token from dashboard>'  # Replace with your actual token
        mobile_numbers = self.user.phone_No
        message = f"Your OTP code is: {self.otp_code}"

        try:
            response = requests.post(
                "https://sms.aakashsms.com/sms/v3/send/",
                data={
                    'auth_token': auth_token,
                    'to': mobile_numbers,
                    'text': message
                }
            )
            return response.status_code == 200
        except Exception as e:
            return False