from django.contrib import admin
from .models import User, Contact, Appointment
# Register your models here.
@admin.register(User)
class AdminUser(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'mobile']

@admin.register(Contact)
class AdminContact(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'subject', 'message']

@admin.register(Appointment)
class AdminAppointment(admin.ModelAdmin):
    list_display = ['id', 'hospital', 'doctor', 'date', 'time']