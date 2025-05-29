from django.shortcuts import render
from django.http import HttpResponse
from .models import Garden
from django.views.generic.edit import CreateView
from .forms import GardenForm

# Create your views here.
def home(request):
    return render(request, 'main_app/home.html')

class GardenCreate(CreateView):
    model = Garden
    form_class = GardenForm
