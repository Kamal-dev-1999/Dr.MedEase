from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Q
from .models import DoctorAppointment
from patients.models import Appointment
from django.core.mail import send_mail

# Sync updates to the patient-side Appointment model when DoctorAppointment is saved
@receiver(post_save, sender=DoctorAppointment)
def sync_appointment_status(sender, instance, created, **kwargs):
    """
    Sync updates to the patient-side Appointment when DoctorAppointment changes.
    """
    try:
        # Fetch the corresponding patient appointment
        patient_appointment = Appointment.objects.filter(
            doctor=instance.doctor,
            appointment_date=instance.appointment_date,
            appointment_time=instance.appointment_time,
        ).filter(
            Q(patient_name__iexact=instance.patient_name.strip()) &
            Q(patient_contact__iexact=instance.patient_contact.strip())
        ).first()

        if not patient_appointment:
            raise Appointment.DoesNotExist()

        # Sync the confirmation status or other fields
        patient_appointment.is_confirmed = instance.is_confirmed
        patient_appointment.save()

        # Optionally send an email notification to the patient
        if instance.is_confirmed:
            send_mail(
                'Your Appointment has been Confirmed',
                f'Your appointment with Dr. {instance.doctor.user.username} on {instance.appointment_date} at {instance.appointment_time} has been confirmed.',
                'from@example.com',
                [patient_appointment.patient_contact],
                fail_silently=False,
            )

        print(f"Successfully synced DoctorAppointment ID {instance.id} to Appointment ID {patient_appointment.id}")
    except Appointment.DoesNotExist:
        print(f"No corresponding patient appointment found for DoctorAppointment ID {instance.id}")





from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import DoctorProfile

@receiver(post_save, sender=User)
def create_doctor_profile(sender, instance, created, **kwargs):
    if created and hasattr(instance, 'doctor_profile'):
        DoctorProfile.objects.create(user=instance)
