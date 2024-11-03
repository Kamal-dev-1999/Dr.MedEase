from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from .models import *
from .serializers import (
    SignupSerializer, LoginSerializer, DoctorProfileSerializer,
    ProfessionalInformationSerializer, WorkDetailsSerializer,
    AdditionalInformationSerializer, SystemFieldsSerializer
)

# Utility function to get doctor_id from the logged-in user
def get_doctor_id(request):
    if request.user.is_authenticated:
        doctor_profile = DoctorProfile.objects.filter(user=request.user).first()
        return doctor_profile.id if doctor_profile else None
    return None

# Doctor Home and Auth Views
class HomePageView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        doctor_id = None
        if request.user.is_authenticated:
            doctor_profile = DoctorProfile.objects.filter(user=request.user).first()
            doctor_id = doctor_profile.id if doctor_profile else None
        
        # Pass doctor_id in context
        return render(request, 'marketplace/base.html', {'doctor_id': doctor_id})


class SignupView(generics.GenericAPIView):
    serializer_class = SignupSerializer
    template_name = 'marketplace/signup.html'

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer()
        return render(request, self.template_name, {'form': serializer})

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            return redirect(reverse_lazy('Doctor:home'))
        return render(request, self.template_name, {'form': serializer, 'errors': serializer.errors})

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    template_name = 'marketplace/signin.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.POST)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            return redirect(reverse_lazy('Doctor:home'))
        return render(request, self.template_name, {
            'form': serializer,
            'error': 'Invalid credentials. Please try again.'
        })

def logout_view(request):
    logout(request)
    return redirect(reverse_lazy('Doctor:home'))







# # Profile Views
# def add_doctor_view(request):
#     if request.method == 'POST':
#         serializer = DoctorProfileSerializer(data=request.POST)
#         if serializer.is_valid():
#             serializer.save()
#             messages.success(request, "Doctor added successfully.")
#             return redirect('doctor_list')
#         else:
#             messages.error(request, "There were errors in the form submission.")
#     else:
#         serializer = DoctorProfileSerializer()
#     return render(request, 'doctor/basic_details.html', {'serializer': serializer})

# class DoctorListCreateAPIView(generics.ListCreateAPIView):
#     queryset = DoctorProfile.objects.all()
#     serializer_class = DoctorProfileSerializer

#     def post(self, request, *args, **kwargs):
#         response = super().post(request, *args, **kwargs)
#         if response.status_code == status.HTTP_201_CREATED:
#             return redirect('doctor-list-create')
#         return render(request, 'doctor/doctor_list.html', {
#             'form': response.data,
#             'errors': response.data.get('errors', {})
#         })



# views.py
# views.py
# views.py
class DoctorDetailAPIView(View):
    def get(self, request, doctor_id):
        # Retrieve the doctor profile based on the provided doctor_id
        doctor = DoctorProfile.objects.filter(id=doctor_id, user=request.user).first()
        if not doctor:
            messages.error(request, "Doctor profile not found.")
            return redirect('doctor-list-create')

        # Fetch professional info, work details, and additional info if they exist
        professional_info = ProfessionalInformation.objects.filter(doctor_account=doctor).first()
        work_info = WorkDetails.objects.filter(doctor_account=doctor).first()
        additional_info = AdditionalInformation.objects.filter(doctor_account=doctor).first()

        # Determine if profile is incomplete based on required fields
        incomplete_profile = not all([
            doctor.first_name, 
            doctor.last_name, 
            doctor.contact_number, 
            professional_info and professional_info.specialization
        ])

        # Use the serializer for doctor data
        doctor_serializer = DoctorProfileSerializer(doctor)

        return render(request, 'doctor/profile.html', {
            'doctor': doctor_serializer.data,
            'professional_info': professional_info,
            'work_info': work_info,
            'additional_info': additional_info,  # Add additional_info to the context
            'form_mode': incomplete_profile,
            'serializer': doctor_serializer if incomplete_profile else None,
        })




class ProfessionalInfoAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfessionalInformationSerializer
    template_name = 'doctor/professional_information_form.html'
    
    def get_queryset(self):
        # Override to filter by the logged-in user's doctor profile
        doctor_profile = DoctorProfile.objects.filter(user=self.request.user).first()
        if doctor_profile:
            return ProfessionalInformation.objects.filter(doctor_account=doctor_profile)
        return ProfessionalInformation.objects.none()  # Return empty if no doctor profile found

    def get(self, request, *args, **kwargs):
        # Check if there is already a professional information record
        doctor_profile = DoctorProfile.objects.filter(user=request.user).first()
        professional_info = ProfessionalInformation.objects.filter(doctor_account=doctor_profile).first()
        
        # If there is no professional info, create a blank serializer
        if professional_info is None:
            serializer = self.get_serializer()  # This creates an empty serializer
        else:
            serializer = self.get_serializer(professional_info)

        return render(request, self.template_name, {
            'professional_info': serializer.data,
            'doctor_id': doctor_profile.id if doctor_profile else None,
        })

    def post(self, request, *args, **kwargs):
        # Get the doctor's profile associated with the logged-in user
        doctor_profile = DoctorProfile.objects.filter(user=request.user).first()
        if not doctor_profile:
            return Response({"error": "Doctor profile not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if there's existing professional information to update or create new
        professional_info = ProfessionalInformation.objects.filter(doctor_account=doctor_profile).first()
        
        if professional_info:
            # Update existing professional information
            serializer = self.get_serializer(professional_info, data=request.data)
        else:
            # Create new professional information
            serializer = self.get_serializer(data=request.data)

        # Validate and save
        if serializer.is_valid():
            serializer.save(doctor_account=doctor_profile)  # Set the doctor_account field
            return redirect(reverse_lazy('Doctor:home'))  # Redirect to the home page instead of doctor's detail page

        # Log errors for debugging
        print(serializer.errors)  # Print errors if validation fails

        # Render the form again with errors
        return render(request, self.template_name, {
            'professional_info': serializer.errors,  # Pass in the errors to show in the form
            'doctor_id': doctor_profile.id if doctor_profile else None,
            'serializer': serializer  # Pass the serializer to retain user input and error messages
        })





class WorkDetailsAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = WorkDetailsSerializer
    template_name = 'doctor/work_details.html'
    
    def get_queryset(self):
        # Filter by the logged-in user's doctor profile
        doctor_profile = DoctorProfile.objects.filter(user=self.request.user).first()
        if doctor_profile:
            return WorkDetails.objects.filter(doctor_account=doctor_profile)
        return WorkDetails.objects.none()  # Return empty if no doctor profile found

    def get(self, request, *args, **kwargs):
        # Check if there is already a work details record
        doctor_profile = DoctorProfile.objects.filter(user=request.user).first()
        
        if not doctor_profile:
            print("No doctor profile found for user:", request.user)
            return render(request, self.template_name, {
                'work_info': None,
                'doctor_id': None,
            })

        print("Doctor Profile found:", doctor_profile)

        work_info = WorkDetails.objects.filter(doctor_account=doctor_profile).first()
        
        # Log whether a work details record was found
        if work_info is None:
            print("No work details found for doctor profile:", doctor_profile)
            serializer = self.get_serializer()  # This creates an empty serializer
        else:
            print("Work details found:", work_info)
            serializer = self.get_serializer(work_info)

        # Log serializer data for debugging
        print("Serializer data:", serializer.data)

        return render(request, self.template_name, {
            'work_info': serializer.data,
            'doctor_id': doctor_profile.id if doctor_profile else None,
        })


    def post(self, request, *args, **kwargs):
        # Get the doctor's profile associated with the logged-in user
        doctor_profile = DoctorProfile.objects.filter(user=request.user).first()
        if not doctor_profile:
            print("Doctor profile not found for user:", request.user)
            return Response({"error": "Doctor profile not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if there's existing work details to update or create new
        work_info = WorkDetails.objects.filter(doctor_account=doctor_profile).first()
        
        if work_info:
            # Update existing work details
            serializer = self.get_serializer(work_info, data=request.data)
        else:
            # Create new work details
            serializer = self.get_serializer(data=request.data)

        # Validate and save
        if serializer.is_valid():
            serializer.save(doctor_account=doctor_profile)  # Set the doctor_account field
            print("Work details saved successfully.")
            return redirect(reverse_lazy('Doctor:home'))  # Redirect to the home page

        # Log errors for debugging
        print("Validation errors:", serializer.errors)  # Print errors if validation fails

        # Render the form again with errors
        return render(request, self.template_name, {
            'work_info': serializer.errors,  # Pass in the errors to show in the form
            'doctor_id': doctor_profile.id,
            'serializer': serializer  # Pass the serializer to retain user input and error messages
        })





class AdditionalInformationAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = AdditionalInformationSerializer
    template_name = 'doctor/additional_information.html'  # Update with the appropriate template path
    
    def get_queryset(self):
        # Filter by the logged-in user's doctor profile
        doctor_profile = DoctorProfile.objects.filter(user=self.request.user).first()
        if doctor_profile:
            return AdditionalInformation.objects.filter(doctor_account=doctor_profile)
        return AdditionalInformation.objects.none()  # Return empty if no doctor profile found

    def get(self, request, *args, **kwargs):
        # Check if there is already additional information record
        doctor_profile = DoctorProfile.objects.filter(user=request.user).first()
        additional_info = AdditionalInformation.objects.filter(doctor_account=doctor_profile).first()

        if additional_info is None:
            serializer = self.get_serializer()  # This creates an empty serializer
        else:
            serializer = self.get_serializer(additional_info)

        return render(request, self.template_name, {
            'additional_info': serializer.data,
            'doctor_id': doctor_profile.id if doctor_profile else None,
        })

    def post(self, request, *args, **kwargs):
        # Get the doctor's profile associated with the logged-in user
        doctor_profile = DoctorProfile.objects.filter(user=request.user).first()
        if not doctor_profile:
            return Response({"error": "Doctor profile not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if there's existing additional information to update or create new
        additional_info = AdditionalInformation.objects.filter(doctor_account=doctor_profile).first()
        
        if additional_info:
            # Update existing additional information
            serializer = self.get_serializer(additional_info, data=request.data)
        else:
            # Create new additional information
            serializer = self.get_serializer(data=request.data)

        # Validate and save
        if serializer.is_valid():
            serializer.save(doctor_account=doctor_profile)  # Set the doctor_account field
            messages.success(request, "Additional information saved successfully.")
            return redirect('Doctor:home')  # Redirect to the home page

        # Log errors for debugging
        print(serializer.errors)  # Print errors if validation fails

        # Render the form again with errors
        return render(request, self.template_name, {
            'additional_info': serializer.errors,  # Pass in the errors to show in the form
            'doctor_id': doctor_profile.id if doctor_profile else None,
            'serializer': serializer  # Pass the serializer to retain user input and error messages
        })

class SystemFieldsAPIView(generics.RetrieveUpdateAPIView):
    queryset = SystemFields.objects.all()
    serializer_class = SystemFieldsSerializer

# @login_required
# def doctor_profile_view(request):
#     doctor_profile = DoctorProfile.objects.filter(user=request.user).first()
#     if not doctor_profile:
#         messages.error(request, "Doctor profile not found.")
#         return redirect('Doctor:home')

#     return render(request, 'doctor/doctor_profile.html', {
#         'doctor_profile': doctor_profile
#     })


from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import ProfessionalInformation, WorkDetails, AdditionalInformation
from .serializers import (
    ProfessionalInformationSerializer,
    WorkDetailsSerializer,
    AdditionalInformationSerializer
)
from rest_framework.response import Response
from rest_framework import status

class UpdateProfessionalInfoView(View):
    def get(self, request):
        instance = get_object_or_404(ProfessionalInformation, doctor_account__user=request.user)
        serializer = ProfessionalInformationSerializer(instance)
        return render(request, 'doctor/update_professional_info.html', {'serializer': serializer})

    def post(self, request):
        instance = get_object_or_404(ProfessionalInformation, doctor_account__user=request.user)
        serializer = ProfessionalInformationSerializer(instance, data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return redirect('Doctor:home')  # Redirect after successful update
        return render(request, 'doctor/update_professional_info.html', {'serializer': serializer})

class UpdateWorkDetailsView(View):
    def get(self, request):
        instance = get_object_or_404(WorkDetails, doctor_account__user=request.user)
        serializer = WorkDetailsSerializer(instance)
        return render(request, 'doctor/update_work_details.html', {'serializer': serializer})

    def post(self, request):
        instance = get_object_or_404(WorkDetails, doctor_account__user=request.user)
        serializer = WorkDetailsSerializer(instance, data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return redirect('Doctor:home')  # Redirect after successful update
        return render(request, 'doctor/update_work_details.html', {'serializer': serializer})

class UpdateAdditionalInfoView(View):
    def get(self, request):
        instance = get_object_or_404(AdditionalInformation, doctor_account__user=request.user)
        serializer = AdditionalInformationSerializer(instance)
        return render(request, 'doctor/update_additional_info.html', {'serializer': serializer})

    def post(self, request):
        instance = get_object_or_404(AdditionalInformation, doctor_account__user=request.user)
        serializer = AdditionalInformationSerializer(instance, data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return redirect('Doctor:home')  # Redirect after successful update
        return render(request, 'doctor/update_additional_info.html', {'serializer': serializer})







