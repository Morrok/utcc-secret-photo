from django.db import models
# from django.contrib.auth.models import User
from cryptography.fernet import Fernet
import base64
import hashlib
import json
import uuid

# key = Fernet.generate_key()


class UserProfile(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=255, unique=True)
    # original_image = models.ImageField(upload_to='files/img/')
    image_data = models.BinaryField()
    # Store the SHA-256 hash of the click coordinates
    click_coordinates_hash = models.CharField(
        max_length=64)  # A SHA-256 hash is 64 characters long
    number_of_click = models.IntegerField()
    failed_login_attempts = models.IntegerField(default=0)
    is_locked = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, auto_now=True)
    date_registered = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def encrypt_image_data(image_file, key):
        """
        Encrypt image data using symmetric encryption and the provided key
        """
        print(key)
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
        print('test33333')
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

    # def save(self, *args, **kwargs):
    #     self.image_data = self.encrypt_image_data(self.image_data)
    #     super().save(*args, **kwargs)


class CookieConsent(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    consent_given = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.consent_given}'


class PictureDescription(models.Model):
    picture = models.ImageField(upload_to='uploads/')
    description = models.TextField()
