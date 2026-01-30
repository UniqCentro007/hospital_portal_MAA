from django.conf import settings

def encrypt_data(value):
    if value is None:
        return None
    return settings.FERNET.encrypt(value.encode()).decode()


def decrypt_data(value):
    if value is None:
        return None
    return settings.FERNET.decrypt(value.encode()).decode()
