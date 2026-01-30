from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Prescription, LabReport
from .serializers import PrescriptionSerializer, LabReportSerializer

from appointments.models import Appointment
from appointments.permissions import IsDoctor, IsPatient

from users.models import DoctorProfile, PatientProfile
from users.permissions import IsAdmin

from audits.utils import log_action




class PrescriptionCreateView(generics.CreateAPIView):
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated, IsDoctor]

    def perform_create(self, serializer):
        appointment = Appointment.objects.get(
            id=self.request.data.get("appointment")
        )

        serializer.save(
            appointment=appointment,
            doctor=appointment.slot.doctor,
            patient=appointment.patient,
        )

        log_action(
            self.request.user,
            f"Created prescription for appointment {appointment.id}",
            self.request
        )

class PrescriptionApproveView(generics.UpdateAPIView):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def perform_update(self, serializer):
        serializer.save(status="APPROVED")

        log_action(
            self.request.user,
            f"Approved prescription ID {serializer.instance.id}",
            self.request
        )

class PatientPrescriptionListView(generics.ListAPIView):
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated, IsPatient]

    def get_queryset(self):
        patient = PatientProfile.objects.get(user=self.request.user)
        return Prescription.objects.filter(
            patient=patient,
            status="APPROVED"
        )

class LabReportUploadView(generics.CreateAPIView):
    serializer_class = LabReportSerializer
    permission_classes = [IsAuthenticated, IsDoctor]

    def perform_create(self, serializer):
        patient = PatientProfile.objects.get(
            id=self.request.data.get("patient")
        )
        doctor = DoctorProfile.objects.get(user=self.request.user)

        serializer.save(
            patient=patient,
            uploaded_by=doctor
        )

        log_action(
            self.request.user,
            f"Uploaded lab report for patient {patient.id}",
            self.request
        )

class LabReportApproveView(generics.UpdateAPIView):
    queryset = LabReport.objects.all()
    serializer_class = LabReportSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def perform_update(self, serializer):
        serializer.save(status="APPROVED")

        log_action(
            self.request.user,
            f"Approved lab report ID {serializer.instance.id}",
            self.request
        )

class PatientLabReportListView(generics.ListAPIView):
    serializer_class = LabReportSerializer
    permission_classes = [IsAuthenticated, IsPatient]

    def get_queryset(self):
        patient = PatientProfile.objects.get(user=self.request.user)
        return LabReport.objects.filter(
            patient=patient,
            status="APPROVED"
        )

class MedicalHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.role == "PATIENT":
            patient = PatientProfile.objects.get(user=user)

        elif user.role == "DOCTOR":
            patient_id = request.query_params.get("patient_id")
            if not patient_id:
                return Response(
                    {"error": "patient_id is required"},
                    status=400
                )
            patient = PatientProfile.objects.get(id=patient_id)

        else:
            return Response({"error": "Access denied"}, status=403)

        timeline = []

        appointments = Appointment.objects.filter(patient=patient)
        for appt in appointments:
            timeline.append({
                "type": "Appointment",
                "date": appt.created_at,
                "details": {
                    "doctor": appt.slot.doctor.user.username,
                    "date": appt.slot.date,
                    "time": f"{appt.slot.start_time} - {appt.slot.end_time}",
                    "status": appt.status,
                }
            })

        prescriptions = Prescription.objects.filter(
            patient=patient,
            status="APPROVED"
        )
        for p in prescriptions:
            timeline.append({
                "type": "Prescription",
                "date": p.created_at,
                "details": {
                    "doctor": p.doctor.user.username,
                    "diagnosis": p.diagnosis,
                    "medicines": p.medicines,
                    "notes": p.notes,
                }
            })

        reports = LabReport.objects.filter(
            patient=patient,
            status="APPROVED"
        )
        for r in reports:
            timeline.append({
                "type": "LabReport",
                "date": r.uploaded_at,
                "details": {
                    "report_name": r.report_name,
                    "file": r.report_file.url,
                }
            })

        timeline.sort(key=lambda x: x["date"], reverse=True)

        log_action(
            request.user,
            f"Viewed medical history of patient {patient.id}",
            request
        )

        return Response(timeline)
