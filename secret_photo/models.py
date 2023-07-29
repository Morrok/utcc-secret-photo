from django.db import models
# from django.contrib.auth.models import User
from cryptography.fernet import Fernet
import base64
import hashlib
import json
# key = Fernet.generate_key()

# users/models.py
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.db import models
from django.utils import timezone
import uuid
from django.contrib.auth import get_user_model
from django.conf import settings


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    user_key = models.CharField(max_length=33, default=uuid.uuid4().hex)

    image_data = models.BinaryField(null=True, default=None)
    number_of_click = models.IntegerField(default=0)
    failed_login_attempts = models.IntegerField(default=0)
    is_locked = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # @property
    # def is_anonymous(self):
    #     return False

    # @property
    # def is_authenticated(self):
    #     return True

    @staticmethod
    def encrypt_image_data(image_file, key):
        """
        Encrypt image data using symmetric encryption and the provided key
        """
        # print(key)
        fernet = Fernet(key)
        image_data = image_file.read()
        encrypted_data = fernet.encrypt(image_data)
        # print(encrypted_data)
        return base64.b64encode(encrypted_data)

    @staticmethod
    def decrypt_image_data(encrypted_data_base64, key):
        """
        Decrypt previously encrypted image data
        """
        fernet = Fernet(key)
        encrypted_data = base64.b64decode(encrypted_data_base64)
        image_data = fernet.decrypt(encrypted_data)
        return image_data

    def get_click_coordinates_hash(self, coordinates):
        # Serialize coordinates
        data = json.dumps(coordinates).encode()

        # Hash the data using SHA-256
        sha256_hash = hashlib.sha256(data).hexdigest()

        return sha256_hash

    def check_click_coordinates(self, coordinates):
        # Serialize coordinates
        data = json.dumps(coordinates).encode()

        # Hash the data using SHA-256
        sha256_hash = hashlib.sha256(data).hexdigest()

        # Compare the hash with the stored hash
        return sha256_hash == self.click_coordinates_hash
    # def set_verification_code(self, verification_code):
    #     self.verification_code = verification_code

    # def check_verification_code(self, verification_code):
    #     return self.verification_code == verification_code


# class UserProfile(models.Model):
#     # user = models.OneToOneField(User, on_delete=models.CASCADE)
#     email = models.CharField(max_length=255, unique=True)
#     user_key = models.CharField(max_length=33)
#     # original_image = models.ImageField(upload_to='files/img/')
#     image_data = models.BinaryField()
#     # Store the SHA-256 hash of the click coordinates
#     click_coordinates_hash = models.CharField(
#         max_length=64)  # A SHA-256 hash is 64 characters long
#     number_of_click = models.IntegerField()
#     failed_login_attempts = models.IntegerField(default=0)
#     is_locked = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     last_login = models.DateTimeField(null=True, auto_now=True)
#     date_registered = models.DateTimeField(auto_now_add=True)

    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = []

    # def is_anonymous(self):
    #     return True

    # def is_authenticated(self):
    #     return True

    # def save(self, *args, **kwargs):
    #     self.image_data = self.encrypt_image_data(self.image_data)
    #     super().save(*args, **kwargs)

def register_user(validated_data, coordinates_zone):
    custom_user = get_user_model()
    coordinates = json.loads(coordinates_zone)
    sorted_data = sorted(
        coordinates, key=lambda item: (item[0], item[1]))
    coordinates = json.dumps(sorted_data)
    user = custom_user.objects.filter(
        email=validated_data.get('email'))
    if not user:
        profile = CustomUser()
        profile.user_key = uuid.uuid4().hex
        profile.email = validated_data.get('email')
        profile.password = \
            CustomUser().get_click_coordinates_hash(coordinates)
        profile.image_data = CustomUser().encrypt_image_data(
            validated_data.get('image_data'),
            settings.AUTHEN_SECRET_KEY.encode('utf-8'))
        profile.number_of_click = validated_data.get(
            'number_of_click')
        profile.save()
        return True
    return False


def reset_password(user, validated_data, coordinates_zone):
    # custom_user = get_user_model()
    coordinates = json.loads(coordinates_zone)
    sorted_data = sorted(
        coordinates, key=lambda item: (item[0], item[1]))
    coordinates = json.dumps(sorted_data)
    # user = CustomUser().objects.get(email=validated_data.get('email'))
    user.password = \
        CustomUser().get_click_coordinates_hash(coordinates)
    user.image_data = CustomUser().encrypt_image_data(
        validated_data.get('image_data'),
        settings.AUTHEN_SECRET_KEY.encode('utf-8'))
    user.number_of_click = validated_data.get(
        'number_of_click')
    user.save()


class CookieConsent(models.Model):
    user = models.ForeignKey('secret_photo.CustomUser',
                             on_delete=models.CASCADE)
    consent_given = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.consent_given}'


class PictureDescription(models.Model):
    picture = models.ImageField(upload_to='uploads/')
    description = models.TextField()
