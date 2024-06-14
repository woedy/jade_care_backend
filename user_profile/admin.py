from django.contrib import admin

from user_profile.models import PersonalInfo, Address, SocialMedia, EmergencyContact, UserLanguage, Doctor, \
    AppointmentSlot, TimeSlot, Patient, Allergy, Diagnosis, Education, Experience

admin.site.register(PersonalInfo)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Allergy)
admin.site.register(Diagnosis)
admin.site.register(Address)
admin.site.register(SocialMedia)
admin.site.register(EmergencyContact)
admin.site.register(UserLanguage)

admin.site.register(Education)
admin.site.register(Experience)

admin.site.register(AppointmentSlot)
admin.site.register(TimeSlot)
