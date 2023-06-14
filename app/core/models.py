import uuid
from django.db import models

class Sect(models.Model):
    sector = models.CharField(max_length=100)

    def __str__(self):
        return self.sector

    class Meta:
        verbose_name = 'Sector'
        verbose_name_plural = 'Sectors'

class SubSect(models.Model):
    sector = models.ForeignKey(Sect, on_delete=models.CASCADE)
    subsector = models.CharField(max_length=100)

    def __str__(self):
        return self.subsector

    class Meta:
        verbose_name = 'Subsector'
        verbose_name_plural = 'Subsectors'

class Indica(models.Model):
    subsector = models.ForeignKey(SubSect, on_delete=models.CASCADE)
    indicator = models.CharField(max_length=100)
    description = models.TextField(default='')

    def __str__(self):
        return self.indicator

    class Meta:
        verbose_name = 'Indicator'
        verbose_name_plural = 'Indicators'

class CountryRank(models.Model):
    year = models.CharField(max_length=255)
    sector = models.CharField(max_length=255)
    subsector = models.CharField(max_length=255)
    indicator = models.CharField(max_length=255)
    amount = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    rank = models.CharField(max_length=255)

    def __str__(self):
        return self.country

    class Meta:
        verbose_name = 'Country Rank'
        verbose_name_plural = 'Country Ranks'