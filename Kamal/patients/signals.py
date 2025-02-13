from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Q
from Doctor.models import DoctorAppointment, DoctorProfile
from patients.models import Appointment

import logging
from django.db import transaction

# Set up logging
logger = logging.getLogger(__name__)

# Signal to create a DoctorAppointment when a patient Appointment is created
@receiver(post_save, sender=Appointment)
def create_doctor_appointment(sender, instance, created, **kwargs):
    if created:  # Only create DoctorAppointment when a new Appointment is created
        # Check if the required fields are filled before creating a DoctorAppointment
        if instance.patient_name and instance.appointment_date and instance.appointment_time:
            doctor_profile = instance.doctor  # Ensure this is valid
            DoctorAppointment.objects.create(
                patient_name=instance.patient_name,
                patient_contact=instance.patient_contact,
                appointment_date=instance.appointment_date,
                appointment_time=instance.appointment_time,
                symptoms=instance.symptoms,
                doctor=doctor_profile,
                is_confirmed=instance.is_confirmed
            )
        else:
            print("Appointment not created due to missing required fields.")


# Signal to sync DoctorAppointment updates to the patient-side Appointment model
@receiver(post_save, sender=DoctorAppointment)
def sync_appointment_status(sender, instance, created, **kwargs):
    """
    Synchronize DoctorAppointment updates to the patient-side Appointment model.
    """
    try:
        with transaction.atomic():
            # Find the corresponding patient appointment
            patient_appointment = Appointment.objects.filter(
                doctor=instance.doctor,
                appointment_date=instance.appointment_date,
                appointment_time=instance.appointment_time,
                patient_name__iexact=instance.patient_name.strip(),
                patient_contact__iexact=instance.patient_contact.strip()
            ).first()

            if not patient_appointment:
                logger.error(f"No corresponding patient appointment found for DoctorAppointment ID {instance.id}")
                return

            # Sync the confirmation status
            patient_appointment.is_confirmed = instance.is_confirmed
            patient_appointment.save()
            logger.info(f"Successfully synced DoctorAppointment ID {instance.id} to Appointment ID {patient_appointment.id}")
    except Exception as e:
        logger.error(f"Error syncing DoctorAppointment ID {instance.id}: {e}")





from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import PatientProfile

@receiver(post_save, sender=User)
def create_patient_profile(sender, instance, created, **kwargs):
    if created and hasattr(instance, 'patient_profile'):
        PatientProfile.objects.create(user=instance)


