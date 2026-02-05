from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import AppointmentSlot, Appointment
from .serializers import AppointmentSlotSerializer, AppointmentSerializer
from .permissions import IsDoctor, IsPatient
from users.models import PatientProfile


class SlotCreateView(generics.CreateAPIView):
    queryset = AppointmentSlot.objects.all()
    serializer_class = AppointmentSlotSerializer
    permission_classes = [IsAuthenticated, IsDoctor]


class AvailableSlotListView(generics.ListAPIView):
    serializer_class = AppointmentSlotSerializer

    def get_queryset(self):
        return AppointmentSlot.objects.filter(is_available=True)


class AppointmentCreateView(generics.CreateAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated, IsPatient]

    def perform_create(self, serializer):
        patient = PatientProfile.objects.get(user=self.request.user)
        slot = serializer.validated_data['slot']
        slot.is_available = False
        slot.save()
        serializer.save(patient=patient)

class AppointmentListView(generics.ListAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == 'DOCTOR':
            return Appointment.objects.filter(slot__doctor__user=user)

        if user.role == 'PATIENT':
            return Appointment.objects.filter(patient__user=user)

        return Appointment.objects.none()

