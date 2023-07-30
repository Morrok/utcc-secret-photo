from cryptography.fernet import Fernet


def encrypt_photo(photo, key):
    fernet = Fernet(key)
    encrypted_photo = fernet.encrypt(photo)
    return encrypted_photo


def decrypt_photo(encrypted_photo, key):
    fernet = Fernet(key)
    decrypted_photo = fernet.decrypt(bytes(encrypted_photo))
    return decrypted_photo
