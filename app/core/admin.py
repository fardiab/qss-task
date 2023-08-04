from django.contrib import admin

from .models import Sect, SubSect, Indica, Country

admin.site.register(Sect)
# admin.site.register(SubSect)
# admin.site.register(Indica)

@admin.register(Indica)
class IndicaAdmin(admin.ModelAdmin):
    list_display = ('indicator', 'subsector')

@admin.register(SubSect)
class SubSectAdmin(admin.ModelAdmin):
    list_display = ('subsector', 'sector')
    search_fields = ('subsector', 'sector')

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('country', 'rank', 'amount', 'year')
    search_fields = ('country', 'year')
