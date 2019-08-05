from django.shortcuts import render

from .models import Gebeurtenis

from .forms import GebeurtenisForm


def index(request):
    gebeurtenissen = Gebeurtenis.objects.all().order_by('-datum')
    context = {'gebeurtenissen': gebeurtenissen}
    return render(request, 'events/index.html', context)


def melding_maken(request):
    form = GebeurtenisForm(request.POST or None)
    print(request.POST)
    if (form.is_valid()):
        form.save()
        form = GebeurtenisForm()
    context = {'form': form}
    return render(request, 'events/melding-maken.html', context)


def over(request):
    return render(request, 'events/over.html')
