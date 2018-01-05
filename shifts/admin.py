from django.contrib import admin

from .models import GroupShift, Shift, Run

admin.site.register(GroupShift)
admin.site.register(Shift)
admin.site.register(Run)