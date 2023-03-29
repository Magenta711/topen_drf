from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class PasswordResets(models.Model):
    id = models.AutoField(primary_key=True)
    token = models.CharField(max_length=90, null=True)
    email = models.CharField(max_length=90, null=True)
    created_at = models.CharField(max_length=90, null=True)