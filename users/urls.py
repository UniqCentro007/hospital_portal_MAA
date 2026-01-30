from django.urls import path
from .views import UserListCreateView
from .views import UserListCreateView, DoctorListView, PatientListView

urlpatterns = [
    
    path('', UserListCreateView.as_view(), name='user-list'),
    path('doctors/', DoctorListView.as_view(), name='doctor-list'),
    path('patients/', PatientListView.as_view(), name='patient-list'),

]

