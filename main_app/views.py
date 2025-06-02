from django.shortcuts import render
# from django.http import HttpResponse
from .models import Garden, User
from django.views.generic.edit import CreateView, UpdateView
from .forms import GardenForm, UserForm

# Create your views here.
def home(request):
    return render(request, 'main_app/home.html')

def start(request):
    return render(request, 'main_app/start.html')

class UserUpdate(UpdateView):
    model = User
    form_class = UserForm
    success_url = '/'
    
    # Update only the logged-in user.
    def get_object(self):
        return self.request.user

class GardenCreate(CreateView):
    model = Garden
    form_class = GardenForm
    success_url = '/profile/'
    
    # Adding this due to null error upon form submission. This makes sure to override the created_by relationship field and assign it automatically to the user. https://docs.djangoproject.com/en/5.2/topics/class-based-views/generic-editing/
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    