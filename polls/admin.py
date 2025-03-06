from django.contrib import admin

# Register your models here.

from.models import Signup, Application, Hawker, License, Inspector, Inspection, EmergencyInspection, Fines, Renewal


admin.site.register(Application)
admin.site.register(Hawker)
admin.site.register(Signup)
admin.site.register(License)
admin.site.register(Inspector)
admin.site.register(Inspection)
admin.site.register(Fines)
admin.site.register(Renewal)
admin.site.register(EmergencyInspection)



