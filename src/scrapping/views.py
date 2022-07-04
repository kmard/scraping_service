from django.shortcuts import render
from .forms import FindForm
from .models import Vacancy

# Create your views here.
def home_view(request):
    # print(request.POST)
    # print(request.GET)
    # GET / home /?city = od & language = Java

    form = FindForm()

    city = request.GET.get('city')
    language = request.GET.get('language')
    qs = []
    if city or language:
        _filter = {}
        if city:
          _filter['city__slug'] = city
        if language:
          _filter['language__slug'] = language

        qs = Vacancy.objects.filter(** _filter)
    else:
        qs = Vacancy.objects.all()

    return render(request,'scrapping/home.html',{'object_list':qs,
                                                 'form':form})
