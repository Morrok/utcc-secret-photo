from django.db import models
from cryptography.fernet import Fernet
import base64
import hashlib
import json
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

    @staticmethod
    def encrypt_image_data(image_file, key):
        fernet = Fernet(key)
        image_data = image_file.read()
        encrypted_data = fernet.encrypt(image_data)
        return base64.b64encode(encrypted_data)

    @staticmethod
    def decrypt_image_data(encrypted_data_base64, key):
        fernet = Fernet(key)
        encrypted_data = base64.b64decode(encrypted_data_base64)
        image_data = fernet.decrypt(encrypted_data)
        return image_data

    def get_click_coordinates_hash(self, coordinates):
        data = json.dumps(coordinates).encode()
        sha256_hash = hashlib.sha256(data).hexdigest()
        return sha256_hash

    def check_click_coordinates(self, coordinates):
        data = json.dumps(coordinates).encode()
        sha256_hash = hashlib.sha256(data).hexdigest()
        return sha256_hash == self.click_coordinates_hash


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
    coordinates = json.loads(coordinates_zone)
    sorted_data = sorted(
        coordinates, key=lambda item: (item[0], item[1]))
    coordinates = json.dumps(sorted_data)
    user.password = \
        CustomUser().get_click_coordinates_hash(coordinates)
    user.image_data = CustomUser().encrypt_image_data(
        validated_data.get('image_data'),
        settings.AUTHEN_SECRET_KEY.encode('utf-8'))
    user.number_of_click = validated_data.get(
        'number_of_click')
    user.failed_login_attempts = 0
    user.save()


def reset_login_failed_attempts(user):
    user.failed_login_attempts = 0
    user.save()


class CookieConsent(models.Model):
    user = models.ForeignKey('secret_photo.CustomUser',
                             on_delete=models.CASCADE)
    consent_given = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.consent_given}'


class PhotoGallery(models.Model):
    custom_user = models.ForeignKey(
        CustomUser, blank=False, null=False, on_delete=models.CASCADE)
    photo_key = models.CharField(max_length=33)
    image_data = models.BinaryField()
    photo_name = models.CharField(max_length=50)
    description = models.BinaryField(blank=True, null=True)
    is_favorite = models.BooleanField(default=False)
    date_updated = models.DateTimeField(null=True)
    date_uploaded = models.DateTimeField(default=timezone.now)

    @staticmethod
    def encrypt_image_data(image_file, key):
        fernet = Fernet(key)
        image_data = image_file.read()
        encrypted_data = fernet.encrypt(image_data)
        return base64.b64encode(encrypted_data)

    @staticmethod
    def decrypt_image_data(encrypted_data_base64, key):
        fernet = Fernet(key)
        encrypted_data = base64.b64decode(encrypted_data_base64)
        image_data = fernet.decrypt(encrypted_data)
        return image_data

    @staticmethod
    def encrypt_description(message, key):
        cipher_suite = Fernet(key)
        encrypted_data = cipher_suite.encrypt(message.encode())
        return base64.b64encode(encrypted_data)

    @staticmethod
    def decrypt_description(message, key):
        cipher_suite = Fernet(key)
        encrypted_data = base64.b64decode(message)
        plain_text = cipher_suite.decrypt(encrypted_data)
        return plain_text.decode()


def add_photo(validated_data, user):
    photo = PhotoGallery()
    photo.custom_user = user
    photo.photo_key = uuid.uuid4().hex
    photo.photo_name = validated_data.get('photo_name')
    photo.description = PhotoGallery().encrypt_description(
        validated_data.get('description'),
        settings.IMAGE_SECRET_KEY.encode('utf-8'))
    photo.image_data = PhotoGallery().encrypt_image_data(
        validated_data.get('image_data'),
        settings.IMAGE_SECRET_KEY.encode('utf-8'))
    photo.is_favorite = validated_data.get('is_favorite')
    photo.save()


def get_list_all_photo():
    return PhotoGallery.objects.all().order_by('-id')


def get_photo_by_photo_key(photo_key):
    return PhotoGallery.objects.get(photo_key=photo_key)


class EncryptedPhoto(models.Model):
    encrypted_image = models.BinaryField()
    description = models.TextField(blank=True, null=True)
