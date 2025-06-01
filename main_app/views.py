from django.shortcuts import render
# from django.http import HttpResponse
from .models import Garden
from django.views.generic.edit import CreateView
from .forms import GardenForm

# Create your views here.
def home(request):
    return render(request, 'main_app/home.html')

class GardenCreate(CreateView):
    model = Garden
    form_class = GardenForm
    success_url = '/profile/'
    
    # Adding this due to null error upon form submission. This makes sure to override the created_by relationship field and assign it automatically to the user. https://docs.djangoproject.com/en/5.2/topics/class-based-views/generic-editing/
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)