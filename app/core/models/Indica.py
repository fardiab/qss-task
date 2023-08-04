from django.db import models
from .SubSect import SubSect


class Indica(models.Model):
    subsector = models.ForeignKey(SubSect, on_delete=models.CASCADE)
    indicator = models.CharField(max_length=250)
    content = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.indicator

    class Meta:
        verbose_name = "Indicator"
        verbose_name_plural = "Indicators"
