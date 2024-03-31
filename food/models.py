from django.db import models

# Create your models here.
class User(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    mobile=models.IntegerField()

class Contact(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    subject=models.CharField(max_length=100)
    message=models.TextField()

class Appointment(models.Model):
    hospital=models.CharField(max_length=100)
    doctor=models.CharField(max_length=100)
    date=models.DateField()
    time=models.CharField(max_length=100)