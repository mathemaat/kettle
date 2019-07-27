from django.db import models


class Doodsoorzaak(models.Model):
    omschrijving = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Doodsoorzaak"
        verbose_name_plural = "Doodsoorzaken"

    def __str__(self):
        return self.omschrijving


class OnderliggendeOorzaak(models.Model):
    doodsoorzaak = models.ForeignKey(Doodsoorzaak, on_delete=models.PROTECT)
    omschrijving = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Onderliggende oorzaak"
        verbose_name_plural = "Onderliggende oorzaken"

    def __str__(self):
        return "{} ({})".format(self.doodsoorzaak.omschrijving, self.omschrijving)


class Gebeurtenis(models.Model):
    datum = models.DateField()
    locatie = models.CharField(max_length=255)
    oorzaak = models.ForeignKey(OnderliggendeOorzaak, on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Gebeurtenis"
        verbose_name_plural = "Gebeurtenissen"

    def __str__(self):
        return "{}, {}, {}".format(self.datum.strftime("%d-%m-%Y"), self.locatie, self.oorzaak)


class Dier(models.Model):
    omschrijving = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Dier"
        verbose_name_plural = "Dieren"

    def __str__(self):
        return self.omschrijving


class Slachtofferaantal(models.Model):
    gebeurtenis = models.ForeignKey(Gebeurtenis, on_delete=models.PROTECT)
    dier = models.ForeignKey(Dier, on_delete=models.PROTECT)
    aantal = models.IntegerField(null=True, blank=True)
    schatting = models.CharField(max_length=16, null=True, blank=True)

    class Meta:
        verbose_name = "Slachtofferaantal"
        verbose_name_plural = "Slachtofferaantallen"
        unique_together = (("gebeurtenis", "dier"),)

    def __str__(self):
        aantal = self.aantal if self.aantal is not None else self.schatting
        return "{} {}".format(aantal, self.dier.omschrijving.lower())
