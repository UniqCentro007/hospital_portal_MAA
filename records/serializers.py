from rest_framework import serializers
from .models import Prescription
from .models import LabReport
from appointments.models import Appointment


class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = '__all__'
        read_only_fields = ['status', 'doctor', 'patient']


class LabReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabReport
        fields = '__all__'
        read_only_fields = ['status']


class MedicalHistorySerializer(serializers.Serializer):
    type = serializers.CharField()
    date = serializers.DateTimeField()
    details = serializers.DictField()


class PrescriptionSerializer(serializers.ModelSerializer):
    diagnosis = serializers.SerializerMethodField()
    medicines = serializers.SerializerMethodField()
    notes = serializers.SerializerMethodField()

    class Meta:
        model = Prescription
        fields = '__all__'

    def get_diagnosis(self, obj):
        return obj.get_diagnosis()

    def get_medicines(self, obj):
        return obj.get_medicines()

    def get_notes(self, obj):
        return obj.get_notes()
