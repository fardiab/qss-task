from django.contrib import admin

from .models import CountryRank
from .models import Sect, SubSect, Indica

admin.site.register(Sect)
admin.site.register(SubSect)
admin.site.register(Indica)



@admin.register(CountryRank)
class CountryRankAdmin(admin.ModelAdmin):
    list_display = ('id', 'country', 'rank')