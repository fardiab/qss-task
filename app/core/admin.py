from django.contrib import admin

from .models import Sect, SubSect, Indica, Country

admin.site.register(Sect)
admin.site.register(SubSect)
admin.site.register(Indica)

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('country', 'rank', 'amount', 'year')
    search_fields = ('country', 'year')
