from typing import Optional
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

from app.utils.base_model import BaseModel

User = get_user_model()

class SignUpUser(BaseModel):
    GENDER = (("male", "male"), ("female", "female"), ("other", "other"))
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="sign_up_user", null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    company = models.CharField(max_length=100, null=True, blank=True)
    industry = models.CharField(max_length=100, null=True, blank=True)
    job_title = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def __str__(self):
        return self.first_name + " " + self.last_name

    class Meta:
        verbose_name = "Sign Up User"
        verbose_name_plural = "Sign Up Users"
