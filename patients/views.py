from rest_framework import status
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import Http404
from .models import Appointment
# from .serializers import AppointmentSerializers
from Doctor.models import DoctorProfile
from django.shortcuts import render, redirect
from django.contrib.auth import login
from rest_framework import generics
from django.urls import reverse_lazy
from .serializers import PatientSignupSerializer  # Assuming you have created a PatientSignupSerializer
from django.contrib.auth import login, authenticate
from rest_framework import generics
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .serializers import PatientLoginSerializer
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.urls import reverse_lazy


class PatientHomePageView(generics.GenericAPIView):
    # Get the PatientProfile instance based on the logged-in user
    def get(self, request):
        patient = request.user.patient_profile

        # Query appointments for that patient instance
        appointments = Appointment.objects.filter(patient=patient)

        return render(request, 'patient/base.html', {'appointments': appointments})



 
 
    
# View to handle patient login
class PatientLoginView(generics.GenericAPIView):
    serializer_class = PatientLoginSerializer  # Use the PatientLoginSerializer for authentication
    template_name = 'marketplace/login.html'  # Path to the login template

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)  # Render the login form

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.POST)  # Pass POST data to the serializer
        if serializer.is_valid():  # Validate the input data
            user = serializer.validated_data['user']  # Retrieve the authenticated user
            login(request, user)  # Log the user in
            return redirect(reverse_lazy('Patient:landing'))  # Redirect to the patient home page
        return render(request, self.template_name, {
            'form': serializer,
            'error': 'Invalid credentials. Please try again.'  # Display error message
        })


# View to handle patient logout
def patient_logout_view(request):
    logout(request)  # Log out the user
    return redirect(reverse_lazy('Doctor:landing'))  # Redirect to the home page

from .models import PatientProfile

class PatientSignupView(generics.GenericAPIView):
    serializer_class = PatientSignupSerializer
    template_name = 'marketplace/patient_signup.html'  # Ensure you have this file

    def post(self, request, *args, **kwargs):
        print("Received data:", request.data)  # Debugging
        serializer = self.get_serializer(data=request.data)  # Use request.POST instead
        print(request.POST)  # Check if username is being sent
        if serializer.is_valid():
            user = serializer.save()

            # Manually assign patient role
            user.is_patient = True
            user.save()

            # Create the patient profile
            patient_profile = PatientProfile(user=user, email=user.email, username=user.username)
            patient_profile.save()

            # Log the user in and redirect
            login(request, user)
            # return redirect(reverse_lazy('Patient:home'))  # Redirect to patient home
        
        
            return Response({'message': 'Account created successfully.'}, status=status.HTTP_201_CREATED)
        return Response({'message': 'Failed to create account.', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        # print("Errors:", serializer.errors)  # Debugging failed validations
        # return render(request, self.template_name, {'form': serializer, 'errors': serializer.errors})

    # def get(self, request, *args, **kwargs):
    #     serializer = self.get_serializer()
        
    #     return render(request, self.template_name, {'form': serializer})



# # Appointment Confirmation View
# class AppointmentConfirmationView(APIView):
#     def get(self, request, *args, **kwargs):
#         # Retrieve the appointment ID passed in the URL
#         try:
#             appointment_id = kwargs.get('appointment_id')
#             appointment = Appointment.objects.get(id=appointment_id)
#         except Appointment.DoesNotExist:
#             raise Http404("Appointment not found")

#         return render(request, 'appointments/confirmation.html', {'appointment': appointment})

# # Create Appointment View
# class AppointmentView(APIView):
#     serializer_class = AppointmentSerializers

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)

#         if serializer.is_valid():
#             # Save the appointment
#             saved_appointment = serializer.save()

#             # Redirect to the confirmation page after creating the appointment
#             return HttpResponseRedirect(reverse('Patient:appointment_confirmation', kwargs={'appointment_id': saved_appointment.id}))

#         # Return validation errors if any
#         return Response({
#             'message': 'Failed to create appointment.',
#             'errors': serializer.errors
#         }, status=status.HTTP_400_BAD_REQUEST)



# # View Appointment and Redirect to Confirmation View
# class ViewAppointment(APIView):
#     def get(self, request, pk):
#         try:
#             # Retrieve the appointment based on pk (appointment_id)
#             appointment = Appointment.objects.get(pk=pk)
#         except Appointment.DoesNotExist:
#             return Response({
#                 'message': 'No appointment exists for this ID'
#             }, status=status.HTTP_404_NOT_FOUND)

#         # Correctly generate the URL for the confirmation page
#         confirmation_url = reverse('Patient:appointment_confirmation', kwargs={'appointment_id': appointment.id})

#         # Redirect to the confirmation page with the appointment_id
#         return redirect(confirmation_url)





from .serializers import AppointmentSerializer


class ViewAppointmentsList(APIView):
    def get(self, request):
        
        patient = request.user.patient_profile  # Assuming the user has a patient profile
        appointments = Appointment.objects.filter(patient=patient)  # Filter by logged-in patient
        serializer = AppointmentSerializer(appointments, many=True)  # Serialize the appointments

        # Render the appointments list in the HTML template
        return render(request, 'patient/appointment_details.html', {
            'appointments': serializer.data
        })



class ViewAppointmentDetail(APIView):
    def get(self, request, pk):
        try:
            patient = request.user.patient_profile  # Assuming the user has a patient profile
            appointment = Appointment.objects.get(pk=pk, patient=patient)  # Get the appointment associated with the patient
        except Appointment.DoesNotExist:
            return Response({
                'message': 'Appointment not found for this patient.'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = AppointmentSerializer(appointment)  # Serialize the appointment data

        # Render the appointment details in the HTML template
        return render(request, 'patient/view_appointment_detail.html', {
            'appointment': serializer.data
        })


class CreateAppointment(APIView):
    def get(self, request):
        # Retrieve all doctors to display in the form
        doctor_profiles = DoctorProfile.objects.all()
        return render(request, 'patient/create_appointment.html', {'doctors': doctor_profiles})

    def post(self, request):
        # Safely retrieve the logged-in user's PatientProfile
        try:
            patient_profile = request.user.appointments
            print(f"Patient: {patient_profile}")

        except AttributeError:
            return render(request, 'patient/create_appointment.html', {
                'errors': {'patient': 'You must be logged in as a patient to create an appointment.'}
            })

        # Get the doctor from the form data
        doctor_id = request.POST.get('doctor')  # Use request.POST for form data
        try:
            doctor = DoctorProfile.objects.get(id=doctor_id)
        except DoctorProfile.DoesNotExist:
            return render(request, 'patient/create_appointment.html', {
                'errors': {'doctor': 'Selected doctor does not exist.'}
            })

        # Prepare data for serialization
        data = {
            'patient': patient_profile.id,  # Pass the patient's ID
            'doctor': doctor.id,
            'appointment_date': request.POST.get('appointment_date'),
            'appointment_time': request.POST.get('appointment_time'),
            'symptoms': request.POST.get('symptoms', ''),
        }

        # Serialize the data
        serializer = AppointmentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return redirect('Patient:view_appointments')  # Redirect to the appointments list
        return render(request, 'patient/create_appointment.html', {'errors': serializer.errors})


    
    
class AppointmentConfirmation(APIView):
    def get(self, request, appointment_id):
        try:
            patient = request.user.patient_profile  # Get the patient from the logged-in user
            appointment = Appointment.objects.get(id=appointment_id, patient=patient)  # Fetch the appointment
        except Appointment.DoesNotExist:
            return Response({
                'message': 'Appointment not found for this patient.'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = AppointmentSerializer(appointment)  # Serialize the appointment details

        return render(request, 'patient/appointment_confirmation.html', {
            'appointment': serializer.data
        })

    def post(self, request, appointment_id):
        try:
            patient = request.user.patient_profile  # Get the patient from the logged-in user
            appointment = Appointment.objects.get(id=appointment_id, patient=patient)  # Fetch the appointment
        except Appointment.DoesNotExist:
            return Response({
                'message': 'Appointment not found for this patient.'
            }, status=status.HTTP_404_NOT_FOUND)

        # Update the appointment status (for confirmation)
        appointment.is_confirmed = True
        appointment.save()

        return redirect('Patient:view_appointments')  # Redirect after confirmation
