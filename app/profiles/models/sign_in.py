from django.db import models


class SignInUser(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Sign In User"
        verbose_name_plural = "Sign In Users"