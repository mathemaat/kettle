from django.contrib import admin

from .models import Doodsoorzaak, OnderliggendeOorzaak, Gebeurtenis, Dier, Slachtofferaantal


class DoodsoorzaakAdmin(admin.ModelAdmin):
    list_display = ('omschrijving',)
    list_display_links = ('omschrijving',)


class OnderliggendeOorzaakAdmin(admin.ModelAdmin):
    list_display = ('omschrijving', 'doodsoorzaak',)
    list_display_links = ('omschrijving',)


class DierAdmin(admin.ModelAdmin):
    list_display = ('omschrijving',)
    list_display_links = ('omschrijving',)


class SlachtofferaantalAdmin(admin.ModelAdmin):
    list_display = ('aantal', 'schatting', 'dier', 'gebeurtenis',)
    list_display_links = ('aantal', 'schatting',)


admin.site.register(Doodsoorzaak, DoodsoorzaakAdmin)
admin.site.register(OnderliggendeOorzaak, OnderliggendeOorzaakAdmin)
admin.site.register(Gebeurtenis)
admin.site.register(Dier, DierAdmin)
admin.site.register(Slachtofferaantal, SlachtofferaantalAdmin)
