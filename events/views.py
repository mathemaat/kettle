from django.shortcuts import render

from .models import Gebeurtenis

from .forms import GebeurtenisForm


def index(request):
    gebeurtenissen = Gebeurtenis.objects.filter(is_bevestigd=True).order_by('-datum')
    context = {'gebeurtenissen': gebeurtenissen}
    return render(request, 'events/index.html', context)


def melding_maken(request):
    form = GebeurtenisForm(request.POST or None)
    if (form.is_valid()):
        form.save()
        return render(request, 'events/melding-opgeslagen.html')
    else:
        context = {'form': form}
        return render(request, 'events/melding-maken.html', context)


def over(request):
    return render(request, 'events/over.html')
