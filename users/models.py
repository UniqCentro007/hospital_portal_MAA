from django.contrib.auth.models import AbstractUser
from django.db import models
from records.encryption import encrypt_data, decrypt_data
from django.conf import settings

User = settings.AUTH_USER_MODEL

class User(AbstractUser):

    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('DOCTOR', 'Doctor'),
        ('PATIENT', 'Patient'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.username} ({self.role})"


class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    experience_years = models.PositiveIntegerField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return f"Dr. {self.user.username} - {self.specialization}"


class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return f"{self.user.username} (Patient)"


class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    address = models.TextField()

    def save(self, *args, **kwargs):
        self.address = encrypt_data(self.address)
        super().save(*args, **kwargs)

    def get_address(self):
        return decrypt_data(self.address)
