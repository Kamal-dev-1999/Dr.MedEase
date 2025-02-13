from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class DoctorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="doctor_profile")
    email = models.EmailField(unique=True, blank=True, null=True)
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    profile_picture = models.ImageField(upload_to='doctor_pics/', blank=True, null=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    # New fields for specialization and experience
    specialty = models.CharField(max_length=100, blank=True, null=True)
    experience = models.TextField(blank=True, null=True)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not hasattr(self, 'professional_info'):
            ProfessionalInformation.objects.create(doctor_account=self)
        if not hasattr(self, 'work_details'):
            WorkDetails.objects.create(doctor_account=self)
        if not hasattr(self, 'additional_info'):
            AdditionalInformation.objects.create(doctor_account=self)
            
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"



class ProfessionalInformation(models.Model):
    doctor_account = models.OneToOneField(DoctorProfile, on_delete=models.CASCADE, related_name="professional_info")
    specialization = models.CharField(max_length=100, blank=True, null=True)  # Allow None
    qualification = models.CharField(max_length=100, blank=True, null=True)  # Allow None
    years_of_experience = models.PositiveIntegerField(blank=True, null=True)  # Allow None
    medical_license_number = models.CharField(max_length=50, blank=True, null=True)  # Allow None
    license_issuing_authority = models.CharField(max_length=100, blank=True, null=True)  # Allow None
    license_expiry_date = models.DateField(blank=True, null=True)  # Allow None
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Allow None

    def __str__(self):
        return f"Professional Info for {self.doctor_account.user.first_name} {self.doctor_account.user.last_name}"


class WorkDetails(models.Model):
    doctor_account = models.OneToOneField(DoctorProfile, on_delete=models.CASCADE, related_name="work_details")
    current_hospital = models.CharField(max_length=200, blank=True, null=True)  # Allow None
    office_address = models.TextField(blank=True, null=True)  # Allow None
    consultation_hours = models.CharField(max_length=50, blank=True, null=True)  # Allow None
    working_days = models.CharField(max_length=100, blank=True, null=True)  # Allow None
    teleconsultation = models.BooleanField(default=False)  # Defaults to False

    def __str__(self):
        return f"Work Details for {self.doctor_account.user.first_name} {self.doctor_account.user.last_name}"


class AdditionalInformation(models.Model):
    doctor_account = models.OneToOneField(DoctorProfile, on_delete=models.CASCADE, related_name="additional_info")
    clinic_name = models.CharField(max_length=200, blank=True, null=True)  # Allow None
    languages_spoken = models.CharField(max_length=200, blank=True, null=True)  # Allow None
    certifications = models.TextField(blank=True, null=True)  # Allow None
    achievements = models.TextField(blank=True, null=True)  # Allow None
    bio = models.TextField(blank=True, null=True)  # Allow None
    special_notes = models.TextField(blank=True, null=True)  # Allow None

    def __str__(self):
        return f"Additional Info for {self.doctor_account.user.first_name} {self.doctor_account.user.last_name}"


class SystemFields(models.Model):
    doctor_account = models.OneToOneField(DoctorProfile, on_delete=models.CASCADE, related_name="system_fields")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)  # Defaults to False

    def __str__(self):
        return f"System Fields for {self.doctor_account.user.first_name} {self.doctor_account.user.last_name}"










# appointment
# DoctorAppointment model
class DoctorAppointment(models.Model):
    # Booking Details (copied from the patient's appointment model)
    patient_name = models.CharField(max_length=255)
    patient_contact = models.CharField(max_length=15)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    symptoms = models.TextField(blank=True, null=True)

    # Reference to the doctor
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name="doctor_appointments",default=1)

    # Status and Metadata
    is_confirmed = models.BooleanField(default=False)  # Sync with patient-side `is_confirmed`
    created_at = models.DateTimeField(auto_now_add=True)  # Track when the request was saved

    def __str__(self):
        return f"Booking for Dr. {self.doctor} on {self.appointment_date}"

    class Meta:
        ordering = ['-created_at']  # Recent bookings appear first