from django.urls import path
from .views import (
    DoctorSignupView,
    LoginView,
    logout_view,
    HomePageView,
    # add_doctor_view,
    # DoctorListCreateAPIView,
    # DoctorDetailAPIView,
    # ProfessionalInfoAPIView,
    # WorkDetailsAPIView,
    # AdditionalInformationAPIView,
    # SystemFieldsAPIView,
    # doctor_profile_view
    DoctorAppointmentsAPIView,
    # doctor_appointments_view,
    DoctorAppointmentsAPIView,
    LandingPageView,
    # ForgotUsernameView,
    # ForgotPassView,
    # # PasswordResetConfirmView
)
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import DoctorDetailsView , DoctorProfileView, EditProfileView , add_profile_picture
app_name = "Doctor"

urlpatterns = [
    # Existing URLs
    path('landing-page', LandingPageView.as_view(), name='landing'),
    path('home-page/', HomePageView.as_view(), name='home'),
    path('signup/', DoctorSignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('doctor-profile/<int:doctor_id>/', DoctorDetailsView.as_view(), name='doctor_profile'),
    path('profile/<int:doctor_id>/', DoctorProfileView.as_view(), name='profile'),
    path('profile/edit/<int:doctor_id>/', EditProfileView.as_view(), name='edit_profile'),
    path('profile/add-picture/<int:doctor_id>/', add_profile_picture, name='add_profile_picture'),
    # path('doctor/<int:doctor_id>/', DoctorDetailAPIView.as_view(), name='doctor_detail'),
    
    # # forgot username or password
    # path('forgot-username/', ForgotUsernameView.as_view(), name='forgot_username'),
    # path('forgot-password/', ForgotPassView.as_view(), name='forgot_password'),
    # path('reset-password/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),


    
    # New URLs
    # 
    # path('doctor/<int:doctor_id>/professional-info/', ProfessionalInfoAPIView.as_view(), name='professional_info'),
    # path('doctor/<int:doctor_id>/professional-info/add', ProfessionalInfoAPIView.as_view(), name='professional_info_add'),
    # path('doctor/<int:doctor_id>/work-details/', WorkDetailsAPIView.as_view(), name='work_details'),
    # path('doctor/<int:doctor_id>/additional-info/', AdditionalInformationAPIView.as_view(), name='additional_info'),
    # path('doctor/<int:doctor_id>/system-fields/', SystemFieldsAPIView.as_view(), name='system_fields'),
    
    # path('', doctor_profile_view, name='doctor_profile'),  # Removed 'profile/' prefix
    
    
    # appointments
    path('appointments/', DoctorAppointmentsAPIView.as_view(), name='doctor-appointments'),
    path('confirm-appointment/',DoctorAppointmentsAPIView.as_view(),name='confirm appointment'),
    path('cancel-appointment/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    path('reschedule-appointment/<int:appointment_id>/', views.reschedule_appointment, name='reschedule_appointment'),
    path('appointments/<int:appointment_id>/confirm/', views.confirm_appointment, name='confirm_appointment'),
    path('appointments/filter/', views.filter_appointments, name='filter_appointments'),
    path('appointments/search/',views.search_patients,name='search_patients')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)