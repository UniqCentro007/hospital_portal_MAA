from rest_framework import serializers
from .models import AppointmentSlot, Appointment


class AppointmentSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppointmentSlot
        fields = '__all__'


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = ['status']

    def validate(self, data):
        slot = data['slot']
        if not slot.is_available:
            raise serializers.ValidationError("This slot is already booked.")
        return data
