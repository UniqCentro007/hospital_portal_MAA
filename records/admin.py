from django.contrib import admin
from .models import Prescription
from .models import Prescription, LabReport

admin.site.register(Prescription)
admin.site.register(LabReport)