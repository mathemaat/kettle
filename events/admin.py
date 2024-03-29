from django.contrib import admin

from .models import Doodsoorzaak, OnderliggendeOorzaak, Gebeurtenis, Dier


class DoodsoorzaakAdmin(admin.ModelAdmin):
    list_display = ('omschrijving',)
    list_display_links = ('omschrijving',)


class OnderliggendeOorzaakAdmin(admin.ModelAdmin):
    list_display = ('omschrijving', 'doodsoorzaak',)
    list_display_links = ('omschrijving',)


class DierAdmin(admin.ModelAdmin):
    list_display = ('omschrijving', 'afbeelding', 'rekeneenheid',)
    list_display_links = ('omschrijving',)

class GebeurtenisAdmin(admin.ModelAdmin):
    list_display = ('datum', 'locatie', 'slachtofferaantal', 'dier', 'oorzaak', 'is_bevestigd',)
    list_display_links = ('datum',)

admin.site.register(Doodsoorzaak, DoodsoorzaakAdmin)
admin.site.register(OnderliggendeOorzaak, OnderliggendeOorzaakAdmin)
admin.site.register(Dier, DierAdmin)
admin.site.register(Gebeurtenis, GebeurtenisAdmin)
