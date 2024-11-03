from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="doctor_profile")
    email = models.EmailField(unique=True, blank=True, null=True)  # Allow None
    username = models.CharField(max_length=50, unique=True, default='default_username')
    first_name = models.CharField(max_length=50, blank=True, null=True)  # Allow None
    last_name = models.CharField(max_length=50, blank=True, null=True)  # Allow None
    # Basic Information
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    profile_picture = models.ImageField(upload_to='doctor_pics/', blank=True, null=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)  # Allow None
    address = models.TextField(blank=True, null=True)  # Allow None

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
