from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from gather.models import Event

class EventAdmin(admin.ModelAdmin):
    model = Event

admin.site.register(Event, EventAdmin)
