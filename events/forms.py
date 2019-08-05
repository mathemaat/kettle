import datetime

from django import forms

from .models import Gebeurtenis, Dier, OnderliggendeOorzaak


class GebeurtenisForm(forms.ModelForm):

    MIN_TOEGESTANE_DATUM = datetime.date(2000, 1, 1)
    MAX_TOEGESTANE_DATUM = datetime.date.today()

    datum = forms.DateField(
        input_formats=['%d-%m-%Y'],
        widget=forms.DateInput(
            attrs={
                'placeholder': 'dd-mm-jjjj',
            }
        ),
        error_messages={
            'required': 'verplicht veld',
            'invalid': 'ongeldige datum (controleer formaat dd-mm-jjjj)'
        },
    )

    locatie = forms.CharField(
        error_messages={
            'required' : 'verplicht veld'
        }
    )

    dier = forms.ModelChoiceField(
        queryset=Dier.objects.order_by('omschrijving'),
        error_messages={
            'required': 'verplicht veld'
        }
    )

    oorzaak = forms.ModelChoiceField(
        queryset=OnderliggendeOorzaak.objects.order_by('doodsoorzaak__omschrijving', 'omschrijving'),
        required=False,
    )

    opmerkingen = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Zijn de keuzemogelijkheden te beperkt? Of heeft u extra informatie, zoals een link naar het nieuwsbericht? Plaats die dan hier.',
            }
        ),
        required=False,
    )

    class Meta:
        model = Gebeurtenis
        fields = [
            'datum',
            'locatie',
            'dier',
            'slachtofferaantal',
            'oorzaak',
            'opmerkingen',
        ]

    def clean_datum(self, *args, **kwargs):
        datum = self.cleaned_data.get('datum')
        if (datum < self.MIN_TOEGESTANE_DATUM):
            raise forms.ValidationError('datum te ver in het verleden')
        if (datum > self.MAX_TOEGESTANE_DATUM):
            raise forms.ValidationError('datum te ver in de toekomst')
        return datum

    def clean_slachtofferaantal(self, *args, **kwargs):
        aantal = self.cleaned_data.get('slachtofferaantal')
        if (aantal is not None and aantal < 1):
            raise forms.ValidationError('ongeldig aantal (minimaal 1)')
        return aantal
