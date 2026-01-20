from django.contrib import admin
from .models import User, DoctorProfile, PatientProfile
from .models import User



admin.site.register(User)
admin.site.register(DoctorProfile)
admin.site.register(PatientProfile)

