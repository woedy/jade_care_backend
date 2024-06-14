from django.contrib import admin

# Register your models here.
from financials.models import Invoice

admin.site.register(Invoice)