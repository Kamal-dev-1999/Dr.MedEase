from django.db import models
from django.contrib.auth.models import User  # Replace with your custom user model if necessary

class TeleconsultationSession(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('upcoming', 'Upcoming'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teleconsult_sessions')
    doctor = models.ForeignKey('Doctor.DoctorProfile', on_delete=models.CASCADE, related_name='teleconsult_sessions')
    appointment_date = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    reason_for_consultation = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Session with Dr. {self.doctor} on {self.appointment_date} ({self.status})"

    class Meta:
        ordering = ['-appointment_date']

