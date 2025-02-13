from django.shortcuts import render, redirect  # Import methods to render templates and handle redirects
from django.contrib.auth.decorators import login_required  # Decorator to restrict access to authenticated users
from django.contrib import messages  # Used to display one-time notifications to users
from rest_framework import generics, status  # DRF generics for building views and HTTP status codes
from rest_framework.views import APIView  # Base class for defining custom API views
from rest_framework.response import Response  # Used to create API responses
from django.views import View  # Class-based views from Django
from django.urls import reverse_lazy  # Simplifies URL resolution in templates
from django.contrib.auth import authenticate, login, logout  # Authentication helpers from Django
from .models import *  # Import all models from the current app
from .serializers import (  # Import necessary serializers
    SignupSerializer, LoginSerializer, DoctorProfileSerializer,
    ProfessionalInformationSerializer, WorkDetailsSerializer,
    AdditionalInformationSerializer, SystemFieldsSerializer
)
from .models import DoctorAppointment
from .serializers import DoctorAppointmentSerializer
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse


class LandingPageView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        doctors = DoctorProfile.objects.all()  # Fetch all doctor profiles
        print(doctors)
        return render(request, 'landingpage/index.html', {'doctors': doctors})
    
    
    
# Utility function to get the doctor_id of the currently logged-in user
def get_doctor_id(request):
    if request.user.is_authenticated:  # Check if the user is logged in
        doctor_profile = DoctorProfile.objects.filter(user=request.user).first()  # Get the doctor's profile linked to the user
        return doctor_profile.id if doctor_profile else None  # Return the doctor's ID if the profile exists
    return None  # Return None if the user is not authenticated

# Home page view for doctors
class HomePageView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        doctor_id = None  # Initialize doctor_id as None
        if request.user.is_authenticated:  # Check if the user is authenticated
            doctor_profile = DoctorProfile.objects.filter(user=request.user).first()  # Fetch the doctor's profile
            doctor_id = doctor_profile.id if doctor_profile else None  # Assign the ID if the profile exists
        return render(request, 'marketplace/base.html', {'doctor_id': doctor_id,
                                                         'doctor_profile':doctor_profile})  # Render the home page with doctor_id



class DoctorSignupView(generics.GenericAPIView):
    serializer_class = SignupSerializer
    template_name = 'marketplace/signup.html'
    
    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer()
        return render(request, self.template_name, {'form': serializer})

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Save the user
            user = serializer.save()

            # Manually assign the doctor role
            user.is_doctor = True
            user.save()

            # Create the doctor profile
            doctor_profile = DoctorProfile(user=user, email=user.email, username=user.username)
            doctor_profile.save()

            # Log the user in and redirect
            login(request, user)
            return redirect(reverse_lazy('Doctor:home'))  # Redirect to the doctor home page

        return render(request, self.template_name, {'form': serializer, 'errors': serializer.errors})




    
    
    
    
    
# View to handle user login
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer  # Use the LoginSerializer for authentication
    template_name = 'marketplace/signin.html'  # Path to the login template

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)  # Render the login form

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.POST)  # Pass POST data to the serializer
        if serializer.is_valid():  # Validate the input data
            user = serializer.validated_data['user']  # Retrieve the authenticated user
            login(request, user)  # Log the user in
            return redirect(reverse_lazy('Doctor:home'))  # Redirect to the home page
        return render(request, self.template_name, {
            'form': serializer,
            'error': 'Invalid credentials. Please try again.'  # Display error message
        })

# View to handle user logout
def logout_view(request):
    logout(request)  # Log out the user
    return redirect(reverse_lazy('Doctor:home'))  # Redirect to the home page



# @login_required
# def doctor_profile_view(request):
#     doctor_profile = DoctorProfile.objects.filter(user=request.user).first()
#     if not doctor_profile:
#         messages.error(request, "Doctor profile not found.")
#         return redirect('Doctor:home')

#     return render(request, 'doctor/doctor_profile.html', {
#         'doctor_profile': doctor_profile
#     })





class DoctorAppointmentsAPIView(APIView):
    """
    API View to manage doctor appointments. Includes retrieval of appointments
    and partial updates (e.g., confirming or canceling an appointment).
    """
    
    def get(self, request):
        if not request.user.is_authenticated:
            # Return error response if the user is not authenticated
            return render(request, 'marketplace/signin.html', {'error': 'Please log in to view your appointments.'})
        # Fetch doctor profile based on the current logged-in user
        doctor_profile = DoctorProfile.objects.filter(user=request.user).first()
        
        if not doctor_profile:
            # Return error response if doctor profile is not found
            return Response({"error": "Doctor profile not found."}, status=404)
        
        # Fetch all appointments for the logged-in doctor
        appointments = DoctorAppointment.objects.filter(doctor=doctor_profile)
        
        # Serialize the retrieved appointments
        serializer = DoctorAppointmentSerializer(appointments, many=True)
        
        # Render appointments in the specified template
        return render(request, 'appointments/view_appointments.html', {
            'appointments': serializer.data,
            'doctor_profile': doctor_profile
        })

    def patch(self, request):
        """
        Partial update of an appointment, such as updating its confirmation status.
        """
        # Get appointment ID and confirmation status from the request data
        appointment_id = request.data.get('appointment_id')
        is_confirmed = request.data.get('is_confirmed')

        try:
            # Retrieve the appointment associated with the logged-in doctor
            appointment = DoctorAppointment.objects.get(id=appointment_id, doctor__user=request.user)
        except DoctorAppointment.DoesNotExist:
            # Return error response if the appointment is not found or unauthorized
            return Response({"error": "Appointment not found or not authorized."}, status=404)

        # Update the confirmation status if provided
        if is_confirmed is not None:
            appointment.is_confirmed = is_confirmed
        appointment.save()

        # Return success message
        return Response({"message": "Appointment updated successfully."})




def confirm_appointment(request, appointment_id):
    """
    Allows a doctor to confirm an appointment.
    """
    # Retrieve the appointment by its ID
    appointment = get_object_or_404(DoctorAppointment, id=appointment_id)

    if request.method == "POST":
        # Check if the appointment is already confirmed
        if not appointment.is_confirmed:
            appointment.is_confirmed = True  # Mark the appointment as confirmed
            appointment.status = "Confirmed"  # Update the status field for clarity
            appointment.save()
            messages.success(request, 'Appointment confirmed successfully.')
        else:
            messages.warning(request, 'Appointment is already confirmed.')

    # Redirect back to the previous page or the appointment list
    return redirect(request.META.get('HTTP_REFERER', 'Doctor:appointments_list'))


def cancel_appointment(request, appointment_id):
    """
    Allows a doctor to cancel an appointment.
    """
    # Retrieve the appointment by its ID
    appointment = get_object_or_404(DoctorAppointment, id=appointment_id)

    if request.method == "POST":
        # Check if the appointment is currently confirmed
        if appointment.is_confirmed:
            appointment.is_confirmed = False  # Mark the appointment as canceled
            appointment.status = "Canceled"  # Update the status field for clarity
            appointment.save()
            messages.success(request, 'Appointment canceled successfully.')
        else:
            messages.warning(request, 'Appointment is already canceled or unconfirmed.')

    # Redirect back to the previous page or the appointment list
    return redirect(request.META.get('HTTP_REFERER', 'Doctor:appointments_list'))


def reschedule_appointment(request, appointment_id):
    """
    Allows a doctor to reschedule an appointment by updating its date and/or time.
    """
    # Retrieve the appointment by its ID
    appointment = get_object_or_404(DoctorAppointment, id=appointment_id)

    if request.method == "POST":
        # Extract new date and time from the request
        new_date = request.POST.get('new_date')
        new_time = request.POST.get('new_time')

        if new_date and new_time:
            if appointment.is_confirmed:
                # Update the appointment's date and time
                appointment.appointment_date = new_date
                appointment.appointment_time = new_time
                appointment.status = "Rescheduled"  # Update the status field for clarity
                appointment.save()
                messages.success(request, 'Appointment rescheduled successfully.')
            else:
                messages.warning(request, 'Cannot reschedule an unconfirmed or canceled appointment.')
        else:
            messages.error(request, 'New date or time is missing.')

    # Redirect back to the previous page or the appointment list
    return redirect(request.META.get('HTTP_REFERER', 'Doctor:appointments_list'))


def filter_appointments(request):
    """
    Filters appointments based on their status: confirmed or canceled.
    """
    # Get the status parameter from the request (either 'confirmed' or 'canceled')
    status_filter = request.GET.get('status', '').lower()

    if status_filter == 'confirmed':
        # Fetch confirmed appointments
        appointments = DoctorAppointment.objects.filter(is_confirmed=True)
    elif status_filter == 'canceled':
        # Fetch canceled appointments
        appointments = DoctorAppointment.objects.filter(is_confirmed=False)
    else:
        # Fetch all appointments if no valid status filter is provided
        appointments = DoctorAppointment.objects.all()

    # Render appointments in the specified template
    return render(request, 'appointments/view_appointments.html', {'appointments': appointments})


def search_patients(request):
    """
    Allows a doctor to search for patients by their names.
    """
    patients = []  # Default to an empty list if no search query is provided
    if request.method == "GET":
        # Extract the search query and convert it to uppercase for case-insensitive search
        search_query = request.GET.get('search_query', '').upper()
        if search_query:
            # Search for patients whose names contain the query
            patients = DoctorAppointment.objects.filter(patient_name__icontains=search_query)
        
        # Render the search results in the specified template
        return render(request, 'appointments/search_results.html', {
            'patients': patients,
            'search_query': search_query
        })





# complete doctor profile 
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .serializers import (
    ProfessionalInformationSerializer,
    WorkDetailsSerializer,
    AdditionalInformationSerializer,
    SystemFieldsSerializer
)
from .models import DoctorProfile

class DoctorDetailsView(APIView):
    
    def get(self, request, *args, **kwargs):
        doctor_profile = request.user.doctor_profile

        # Ensure related objects exist before passing them to the template
        professional_info = getattr(doctor_profile, 'professional_info', None)
        work_details = getattr(doctor_profile, 'work_details', None)
        additional_info = getattr(doctor_profile, 'additional_info', None)

        context = {
            'professional_info': ProfessionalInformationSerializer(instance=professional_info).data if professional_info else None,
            'work_details': WorkDetailsSerializer(instance=work_details).data if work_details else None,
            'additional_info': AdditionalInformationSerializer(instance=additional_info).data if additional_info else None,
        }
        return render(request, 'doctor/details.html', context)

    def post(self, request, *args, **kwargs):
        doctor_profile = request.user.doctor_profile  # Get logged-in doctor's profile
        data = request.POST
        
        # Process Professional Information
        professional_info_data = {
            'specialization': data.get('specialization'),
            'qualification': data.get('qualification'),
            'years_of_experience': data.get('years_of_experience'),
            'medical_license_number': data.get('medical_license_number'),
            'license_issuing_authority': data.get('license_issuing_authority'),
            'license_expiry_date': data.get('license_expiry_date'),
            'consultation_fee': data.get('consultation_fee'),
        }
        professional_serializer = ProfessionalInformationSerializer(
            instance=getattr(doctor_profile, 'professional_info', None),
            data=professional_info_data
        )
        if professional_serializer.is_valid():
            professional_serializer.save(doctor_account=doctor_profile)
        
        # Process Work Details
        work_details_data = {
            'current_hospital': data.get('current_hospital'),
            'office_address': data.get('office_address'),
            'consultation_hours': data.get('consultation_hours'),
            'working_days': data.get('working_days'),
            'teleconsultation': data.get('teleconsultation') == 'on',
        }
        work_serializer = WorkDetailsSerializer(
            instance=getattr(doctor_profile, 'work_details', None),
            data=work_details_data
        )
        if work_serializer.is_valid():
            work_serializer.save(doctor_account=doctor_profile)
        
        # Process Additional Information
        additional_info_data = {
            'languages_spoken': data.get('languages_spoken'),
            'certifications': data.get('certifications'),
            'achievements': data.get('achievements'),
            'bio': data.get('bio'),
            'special_notes': data.get('special_notes'),
        }
        additional_serializer = AdditionalInformationSerializer(
            instance=getattr(doctor_profile, 'additional_info', None),
            data=additional_info_data
        )
        if additional_serializer.is_valid():
            additional_serializer.save(doctor_account=doctor_profile)

        # Redirect to the same page with a success message
        return redirect('Doctor:home')



class DoctorProfileView(generics.GenericAPIView):
    
    def get(self, request, *args, **kwargs):
        doctor_profile = DoctorProfile.objects.get(user=request.user)

        # Use getattr() to safely access related fields
        professional_info = getattr(doctor_profile, 'professional_info', None)
        work_details = getattr(doctor_profile, 'work_details', None)
        additional_info = getattr(doctor_profile, 'additional_info', None)

        return render(request, 'doctor/profile.html', {
            'doctor_profile': doctor_profile,
            'professional_info': professional_info,
            'work_details': work_details,
            'additional_info': additional_info,
        })


class EditProfileView(generics.GenericAPIView):
    
    def get(self, request, *args, **kwargs):
        doctor_profile= DoctorProfile.objects.get(user=request.user)
        
        
        # Ensure related objects exist before passing them to the template
        professional_info = getattr(doctor_profile, 'professional_info', None)
        work_details = getattr(doctor_profile, 'work_details', None)
        additional_info = getattr(doctor_profile, 'additional_info', None)

        # Render the profile editing form
        messages.success(request, f"Profile updated successfully.")
        return render(request, 'doctor/details.html', {
            'doctor_profile': doctor_profile,
            'professional_info': professional_info,
            'work_details': work_details,
            'additional_info': additional_info,
        })
    def post(self, request, *args, **kwargs):
        doctor_profile = request.user.doctor_profile  # Get logged-in doctor's profile
        data = request.POST
        
        # Process Professional Information
        professional_info_data = {
            'specialization': data.get('specialization'),
            'qualification': data.get('qualification'),
            'years_of_experience': data.get('years_of_experience'),
            'medical_license_number': data.get('medical_license_number'),
            'license_issuing_authority': data.get('license_issuing_authority'),
            'license_expiry_date': data.get('license_expiry_date'),
            'consultation_fee': data.get('consultation_fee'),
        }
        professional_serializer = ProfessionalInformationSerializer(
            instance=getattr(doctor_profile, 'professional_info', None),
            data=professional_info_data
        )
        if professional_serializer.is_valid():
            professional_serializer.save(doctor_account=doctor_profile)
        
        # Process Work Details
        work_details_data = {
            'current_hospital': data.get('current_hospital'),
            'office_address': data.get('office_address'),
            'consultation_hours': data.get('consultation_hours'),
            'working_days': data.get('working_days'),
            'teleconsultation': data.get('teleconsultation') == 'on',
        }
        work_serializer = WorkDetailsSerializer(
            instance=getattr(doctor_profile, 'work_details', None),
            data=work_details_data
        )
        if work_serializer.is_valid():
            work_serializer.save(doctor_account=doctor_profile)
        
        # Process Additional Information
        additional_info_data = {
            'languages_spoken': data.get('languages_spoken'),
            'certifications': data.get('certifications'),
            'achievements': data.get('achievements'),
            'bio': data.get('bio'),
            'special_notes': data.get('special_notes'),
        }
        additional_serializer = AdditionalInformationSerializer(
            instance=getattr(doctor_profile, 'additional_info', None),
            data=additional_info_data
        )
        if additional_serializer.is_valid():
            additional_serializer.save(doctor_account=doctor_profile)

        # Redirect to the same page with a success message
        return redirect('Doctor:home')


def add_profile_picture(request, doctor_id):
    """
    Allows a doctor to add or update their profile picture.
    """
    doctor_profile = get_object_or_404(DoctorProfile, id=doctor_id)

    if request.method == "POST":
        profile_picture = request.FILES.get('profile_picture')

        if profile_picture:
            doctor_profile.profile_picture = profile_picture
            doctor_profile.save()
            messages.success(request, 'Profile picture updated successfully.')
        else:
            messages.error(request, 'No image file provided.')

    # Redirect back to previous page or doctor profile
    return redirect(request.META.get('HTTP_REFERER') or reverse('Doctor:doctor_profile', args=[doctor_id]))

  

# The two main concepts you're asking about are:

# getattr()
# hasattr()
# These functions help handle cases where an attribute (e.g., professional_info, work_details) may or may not exist in an object, preventing errors like RelatedObjectDoesNotExist.

# 1. getattr(object, attribute, default_value)
# This function retrieves the value of an attribute from an object.
# If the attribute does not exist, it returns a default value instead of raising an error.


# 2. hasattr(object, attribute)
# This function checks if an object has a specific attribute.
# It returns True if the attribute exists, and False otherwise.
