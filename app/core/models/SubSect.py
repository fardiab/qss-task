from django.db import models
from .Sect import Sect


class SubSect(models.Model):
    sector = models.ForeignKey(Sect, on_delete=models.CASCADE)
    subsector = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.subsector

    class Meta:
        verbose_name = "Subsector"
        verbose_name_plural = "Subsectors"