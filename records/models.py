from django.db import models
from appointments.models import Appointment
from users.models import DoctorProfile, PatientProfile
from .encryption import encrypt_data, decrypt_data



class Prescription(models.Model):

    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    )

    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)

    diagnosis = models.TextField()
    medicines = models.TextField()
    notes = models.TextField(blank=True)

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='PENDING'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prescription for {self.patient}"
    
class LabReport(models.Model):

    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    )

    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    uploaded_by = models.ForeignKey(
        DoctorProfile, on_delete=models.SET_NULL, null=True, blank=True
    )

    report_name = models.CharField(max_length=200)
    report_file = models.FileField(upload_to='lab_reports/')
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='PENDING'
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.report_name} - {self.patient}"    


class Prescription(models.Model):
    ...
    diagnosis = models.TextField()
    medicines = models.TextField()
    notes = models.TextField(blank=True)
    ...
    def save(self, *args, **kwargs):
        self.diagnosis = encrypt_data(self.diagnosis)
        self.medicines = encrypt_data(self.medicines)
        self.notes = encrypt_data(self.notes)
        super().save(*args, **kwargs)

    def get_diagnosis(self):
        return decrypt_data(self.diagnosis)

    def get_medicines(self):
        return decrypt_data(self.medicines)

    def get_notes(self):
        return decrypt_data(self.notes)
