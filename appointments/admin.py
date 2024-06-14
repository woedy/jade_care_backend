from django.contrib import admin

from appointments.models import Appointment, AppointmentForOther, Payment, AppointmentMedium, TransferDoctor

admin.site.register(Appointment)
admin.site.register(AppointmentForOther)
admin.site.register(Payment)
admin.site.register(TransferDoctor)
admin.site.register(AppointmentMedium)