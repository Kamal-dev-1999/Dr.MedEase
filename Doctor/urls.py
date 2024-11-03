from django.urls import path
from .views import (
    SignupView,
    LoginView,
    logout_view,
    HomePageView,
    # add_doctor_view,
    # DoctorListCreateAPIView,
    DoctorDetailAPIView,
    ProfessionalInfoAPIView,
    WorkDetailsAPIView,
    AdditionalInformationAPIView,
    SystemFieldsAPIView,
    # doctor_profile_view
)

app_name = "Doctor"

urlpatterns = [
    # Existing URLs
    path('home-page/', HomePageView.as_view(), name='home'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),

    # New URLs
    # path('add-doctor/', add_doctor_view, name='add_doctor'),
    # path('doctors/', DoctorListCreateAPIView.as_view(), name='doctor_list_create'),
    # urls.py
    path('doctor/<int:doctor_id>/', DoctorDetailAPIView.as_view(), name='doctor_detail'),
    path('doctor/<int:doctor_id>/professional-info/', ProfessionalInfoAPIView.as_view(), name='professional_info'),
    path('doctor/<int:doctor_id>/professional-info/add', ProfessionalInfoAPIView.as_view(), name='professional_info_add'),
    path('doctor/<int:doctor_id>/work-details/', WorkDetailsAPIView.as_view(), name='work_details'),
    path('doctor/<int:doctor_id>/additional-info/', AdditionalInformationAPIView.as_view(), name='additional_info'),
    path('doctor/<int:doctor_id>/system-fields/', SystemFieldsAPIView.as_view(), name='system_fields'),
    
    # path('', doctor_profile_view, name='doctor_profile'),  # Removed 'profile/' prefix
]
