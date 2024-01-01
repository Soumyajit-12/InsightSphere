from django.db import models

# Create your models here.

class Information(models.Model):
    department = models.CharField(max_length=200)
    tag = models.CharField(max_length=200)
    link = models.CharField(max_length=200)