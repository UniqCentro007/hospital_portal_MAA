from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import DoctorProfile, PatientProfile
from .serializers import DoctorProfileSerializer, PatientProfileSerializer
from .models import User
from .serializers import UserSerializer
from .permissions import IsAdmin

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]


class DoctorListView(generics.ListAPIView):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileSerializer
    permission_classes = [IsAuthenticated]


class PatientListView(generics.ListAPIView):
    queryset = PatientProfile.objects.all()
    serializer_class = PatientProfileSerializer
    permission_classes = [IsAuthenticated, IsAdmin]    

