from django.contrib import admin
from .models import DoctorProfile, ProfessionalInformation, WorkDetails, AdditionalInformation, SystemFields

class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ('get_user_name', 'date_of_birth', 'gender', 'contact_number', 'address')

    def get_user_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    get_user_name.short_description = 'User Name'  # This sets the column header in the admin

# Register the models
admin.site.register(DoctorProfile, DoctorProfileAdmin)
admin.site.register(ProfessionalInformation)
admin.site.register(WorkDetails)
admin.site.register(AdditionalInformation)
admin.site.register(SystemFields)
