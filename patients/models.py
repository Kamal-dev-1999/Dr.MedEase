from django.db import models
from Doctor.models import DoctorProfile  # Replace `doctor_app` with the name of the doctor app.
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings


class PatientProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="patient_profile")
    email = models.EmailField(unique=True, blank=True, null=True)
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"



class Appointment(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    symptoms = models.TextField(blank=True, null=True)
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='appointments')
    is_confirmed = models.BooleanField(default=False)

    @property
    def patient_name(self):
        # Dynamically retrieve the full name of the patient
        return f"{self.patient.user.first_name} {self.patient.user.last_name}"

    @property
    def doctor_name(self):
        # Dynamically retrieve the full name of the doctor
        return f"{self.doctor.user.first_name} {self.doctor.user.last_name}"

    def __str__(self):
        return f"Appointment with Dr. {self.doctor_name} for {self.patient_name} on {self.appointment_date}"
