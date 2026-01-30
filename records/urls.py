from django.urls import path
from .views import (
    PrescriptionCreateView,
    PrescriptionApproveView,
    PatientPrescriptionListView,
    LabReportUploadView,
    LabReportApproveView,
    PatientLabReportListView,
    MedicalHistoryView,
)

urlpatterns = [
    path('prescriptions/create/', PrescriptionCreateView.as_view()),
    path('prescriptions/<int:pk>/approve/', PrescriptionApproveView.as_view()),
    path('prescriptions/my/', PatientPrescriptionListView.as_view()),
    path('lab-reports/upload/', LabReportUploadView.as_view()),
    path('lab-reports/<int:pk>/approve/', LabReportApproveView.as_view()),
    path('lab-reports/my/', PatientLabReportListView.as_view()),
    path('medical-history/', MedicalHistoryView.as_view()),
]
