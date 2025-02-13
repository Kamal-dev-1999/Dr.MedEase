# Doctor/context_processors.py
from .models import DoctorProfile

def doctor_id_processor(request):
    doctor_id = None
    if request.user.is_authenticated:
        doctor_profile = DoctorProfile.objects.filter(user=request.user).first()
        doctor_id = doctor_profile.id if doctor_profile else None
    return {'doctor_id': doctor_id}
