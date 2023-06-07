from django.shortcuts import render

from .models import Sect, SubSect, Indica

def all(request):
    sectors = Sect.objects.all()
    subsectors = SubSect.objects.all()
    indicators = Indica.objects.all()
    context = {
        'sectors': sectors,
        'subsectors': subsectors,
        'indicators': indicators,
    }
    return render(request, 'first_page.html', context=context)

def agriculture(request):
    subsectors = SubSect.objects.filter(sector__sector='Agriculture')
    indicators = Indica.objects.all()
    context = {
        'subsectors': subsectors,
    }
    return render(request, 'subsectors/agriculture_subsec.html', context=context)

def army(request):
    subsectors = SubSect.objects.filter(sector__sector='Army')
    indicators = Indica.objects.all()
    context = {
        'subsectors': subsectors,
    }
    return render(request, 'subsectors/army_subsec.html', context=context)


def economy(request):
    subsectors = SubSect.objects.filter(sector__sector='Economy')
    indicators = Indica.objects.all()
    context = {
        'subsectors': subsectors,
    }
    return render(request, 'subsectors/economy_subsec.html', context=context)

def government(request):
    subsectors = SubSect.objects.filter(sector__sector='Government')
    indicators = Indica.objects.all()
    context = {
        'subsectors': subsectors,
    }
    return render(request, 'subsectors/government_subsec.html', context=context)

def health(request):
    subsectors = SubSect.objects.filter(sector__sector='Health')
    indicators = Indica.objects.all()
    context = {
        'subsectors': subsectors,
        }
    return render(request, 'subsectors/health_subsec.html', context=context)

def social(request):
    subsectors = SubSect.objects.filter(sector__sector='Social')
    indicators = Indica.objects.all()
    context = {

            'subsectors': subsectors,

            }
    return render(request, 'subsectors/social_subsec.html', context=context)

def technology(request):
    subsectors = SubSect.objects.filter(sector__sector='Technology')
    indicators = Indica.objects.all()
    context = {
        'subsectors': subsectors,
    }
    return render(request, 'subsectors/technology_subsec.html', context=context)

def transportation(request):
    subsectors = SubSect.objects.filter(sector__sector='Transportation')
    indicators = Indica.objects.all()
    context = {
        'subsectors': subsectors,
    }
    return render(request, 'subsectors/transportation_subsec.html', context=context)

def other(request):
    subsectors = SubSect.objects.filter(sector__sector='Other')
    indicators = Indica.objects.all()
    context = {
        'subsectors': subsectors,
    }
    return render(request, 'subsectors/other_subsec.html', context=context)


def details(request, pk):
    indicator = Indica.objects.filter(subsector=pk)
    context = {
        'indicator': indicator,
    }
    return render(request, 'indicators/details.html', context=context)

def text(request, pk):
    indicator = Indica.objects.filter(pk=pk)
    context = {
        'indicator': indicator,
    }
    return render(request, 'indicators/text.html', context=context)