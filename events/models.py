from django.db import models


class Doodsoorzaak(models.Model):
    omschrijving = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Doodsoorzaak"
        verbose_name_plural = "Doodsoorzaken"
        ordering = ['omschrijving']

    def __str__(self):
        return self.omschrijving


class OnderliggendeOorzaak(models.Model):
    doodsoorzaak = models.ForeignKey(Doodsoorzaak, on_delete=models.PROTECT)
    omschrijving = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Onderliggende oorzaak"
        verbose_name_plural = "Onderliggende oorzaken"
        ordering = ['omschrijving']

    def __str__(self):
        return "{} ({})".format(self.doodsoorzaak.omschrijving, self.omschrijving)


class Dier(models.Model):

    ICON_FOLDER = 'dieren/'
    ICON_FOLDER_GIGA = '128x128/'
    ICON_FOLDER_MEGA = '64x64/'
    ICON_FOLDER_GROOT = '32x32/'

    omschrijving = models.CharField(max_length=255)
    afbeelding = models.CharField(max_length=16, default='')
    rekeneenheid = models.IntegerField(default=1)

    class Meta:
        verbose_name = "Dier"
        verbose_name_plural = "Dieren"
        ordering = ['omschrijving']

    def __str__(self):
        return self.omschrijving


class Gebeurtenis(models.Model):

    OMVANG_UNKNOWN = 'UNKNOWN'
    OMVANG_GIGA = 'GIGA'
    OMVANG_MEGA = 'MEGA'
    OMVANG_GROOT = 'GROOT'

    datum = models.DateField()
    locatie = models.CharField(max_length=255)
    oorzaak = models.ForeignKey(OnderliggendeOorzaak, on_delete=models.PROTECT, null=True, blank=True)
    dier = models.ForeignKey(Dier, on_delete=models.PROTECT)
    slachtofferaantal = models.IntegerField(null=True, blank=True)
    slachtofferbeschrijving_format = models.CharField(max_length=255, default='{slachtofferaantal} {dier}')
    opmerkingen = models.TextField(null=True, blank=True)
    is_bevestigd = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Gebeurtenis"
        verbose_name_plural = "Gebeurtenissen"
        ordering = ['-datum']

    def __str__(self):
        return "{}: {} te {} wegens {}".format(
            self.datum.strftime("%d-%m-%Y"),
            self.get_slachtofferbeschrijving(),
            self.locatie,
            self.oorzaak
        )

    def get_slachtofferbeschrijving(self):
        return self.slachtofferbeschrijving_format.format(
            slachtofferaantal=self.slachtofferaantal,
            dier=self.dier.omschrijving.lower()
        )

    def get_omvang(self):
        if (self.slachtofferaantal is None):
            return self.OMVANG_UNKNOWN
        elif (self.slachtofferaantal >= self.dier.rekeneenheid * 100):
            return self.OMVANG_GIGA
        elif (self.slachtofferaantal >= self.dier.rekeneenheid * 10):
            return self.OMVANG_MEGA
        else:
            return self.OMVANG_GROOT

    def get_rekeneenheden(self):
        return {
            self.OMVANG_GIGA: self.dier.rekeneenheid * 100,
            self.OMVANG_MEGA: self.dier.rekeneenheid * 10,
            self.OMVANG_GROOT: self.dier.rekeneenheid,
        }

    def get_afbeeldingsaantallen(self):
        afbeeldingaantallen = {
            self.OMVANG_GIGA: 0,
            self.OMVANG_MEGA: 0,
            self.OMVANG_GROOT: 0,
        }
        rekeneenheden = self.get_rekeneenheden()

        omvang = self.get_omvang()
        if (omvang == self.OMVANG_UNKNOWN):
            return afbeeldingaantallen
        else:
            rest = self.slachtofferaantal
            for omvang in rekeneenheden:
                rekeneenheid = rekeneenheden[omvang]
                while (rest >= rekeneenheid):
                    afbeeldingaantallen[omvang] += 1
                    rest -= rekeneenheid
            return afbeeldingaantallen

    def get_afbeeldingenreeks(self):
        aantallen = self.get_afbeeldingsaantallen()
        folders = {
            self.OMVANG_GIGA: Dier.ICON_FOLDER_GIGA,
            self.OMVANG_MEGA: Dier.ICON_FOLDER_MEGA,
            self.OMVANG_GROOT: Dier.ICON_FOLDER_GROOT,
        }

        afbeeldingen = []
        for omvang in aantallen:
            aantal = aantallen[omvang]
            path = Dier.ICON_FOLDER + folders[omvang] + self.dier.afbeelding
            afbeeldingen += [path] * aantal
        return afbeeldingen
