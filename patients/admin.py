from django.contrib import admin
from .models import Appointment , PatientProfile
# Register your models here.


admin.site.register(Appointment)
admin.site.register(PatientProfile)