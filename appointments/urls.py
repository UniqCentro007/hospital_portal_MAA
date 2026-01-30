from django.urls import path
from .views import (
    SlotCreateView,
    AvailableSlotListView,
    AppointmentCreateView,
    AppointmentListView,
)

urlpatterns = [
    path('slots/create/', SlotCreateView.as_view()),
    path('slots/available/', AvailableSlotListView.as_view()),
    path('appointments/book/', AppointmentCreateView.as_view()),
    path('appointments/', AppointmentListView.as_view()),
]
