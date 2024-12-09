from django.db import models

# Create your models here.

class User(models.Model):
    phone=models.BigIntegerField()
    password = models.CharField(max_length=20)
    status=models.IntegerField()
    name = models.CharField(max_length=200)
