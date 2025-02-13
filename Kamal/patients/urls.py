from django.urls import path
# from .views import AppointmentConfirmationView, AppointmentView, ViewAppointment 
from .views import PatientLoginView, patient_logout_view , PatientSignupView ,PatientHomePageView
from .views import ViewAppointmentsList, ViewAppointmentDetail, CreateAppointment, AppointmentConfirmation
app_name='Patient'

urlpatterns = [
    path('landing/', PatientHomePageView.as_view(), name='landing'),
    path('login/', PatientLoginView.as_view(), name='patient_login'),
    path('logout/', patient_logout_view, name='patient_logout'),
    path('signup/', PatientSignupView.as_view(), name='patient_signup'),
    # path('book-appointment/', AppointmentView.as_view(), name='create-appointment'),
    # path('appointments/<int:pk>/', ViewAppointment.as_view(), name='view_appointment'),  # View appointment endpoint
    # path('appointments/confirmation/<int:appointment_id>/', AppointmentConfirmationView.as_view(), name='appointment_confirmation'),
    
     path('appointments/', ViewAppointmentsList.as_view(), name='view_appointments'),
    
    # URL for viewing the details of a single appointment
    path('appointments/<int:pk>/', ViewAppointmentDetail.as_view(), name='view_appointment'),
    
    # URL for creating a new appointment
    path('appointments/create/', CreateAppointment.as_view(), name='create_appointment'),
    
    # URL for appointment confirmation
    path('appointments/<int:appointment_id>/confirm/', AppointmentConfirmation.as_view(), name='appointment_confirmation'),
    

]
