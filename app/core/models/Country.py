from django.db import models
from .Indica import Indica


class Country(models.Model):
    indicator = models.ForeignKey(
        Indica, on_delete=models.CASCADE, null=True, blank=True
    )
    country = models.CharField(max_length=100)
    rank = models.BigIntegerField(null=True, blank=True)
    amount = models.CharField(max_length=100, null=True, blank=True)
    year = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.country

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"