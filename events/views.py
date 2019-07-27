from django.shortcuts import render

from .models import Gebeurtenis


def index(request):
    gebeurtenissen = Gebeurtenis.objects.all().order_by('-datum')
    context = {'gebeurtenissen': gebeurtenissen}
    return render(request, 'events/index.html', context)
