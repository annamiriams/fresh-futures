from django.shortcuts import render
# from django.http import HttpResponse
from .models import Garden, User
from django.views.generic.edit import CreateView, UpdateView
from .forms import GardenForm
# from .forms import UserForm
from django.urls import reverse_lazy
from django.conf import settings

# Create your views here.
def home(request):
    return render(request, 'main_app/home.html')

def profile(request):
    user = request.user
    gardens = Garden.objects.filter(created_by=user)
    return render(request, 'main_app/profile.html', {
        'user': user,
        'gardens': gardens,
        'mapbox_token': settings.MAPBOX_ACCESS_TOKEN,  # Pass the token to the template
    })

def test_maps(request):
    """
    Test view to verify both map types are working
    Simulates both gardener profile and discover gardens scenarios
    """
    from django.contrib.auth import get_user_model
    from .models import Garden
    
    User = get_user_model()
    
    # Get some test data - use existing users and gardens from your database
    # If you don't have any yet, we'll create mock data
    
    # Try to get real gardens from database
    all_gardens = Garden.objects.filter(
        latitude__isnull=False,
        longitude__isnull=False
    ).select_related('created_by')[:10]  # Limit to 10 for testing
    
    # Try to get a real user
    test_gardener = User.objects.filter(
        latitude__isnull=False,
        longitude__isnull=False
    ).first()
    
    # If no real data, create mock data for testing
    if not all_gardens.exists():
        # Mock garden data for testing
        mock_gardens = [
            {
                'id': 1,
                'name': 'Downtown Community Garden',
                'description': 'A vibrant community space in the heart of the city',
                'address': '123 Main St, San Francisco, CA',
                'latitude': 37.7749,
                'longitude': -122.4194,
                'created_by': {'get_full_name': lambda: 'Alice Johnson'},
                'timeline': 'within 1 month'
            },
            {
                'id': 2,
                'name': 'Sunset Garden Project',
                'description': 'Growing organic vegetables for local families',
                'address': '456 Sunset Blvd, San Francisco, CA',
                'latitude': 37.7849,
                'longitude': -122.4294,
                'created_by': {'get_full_name': lambda: 'Bob Smith'},
                'timeline': '1-3 months'
            },
            {
                'id': 3,
                'name': 'Mission Bay Green Space',
                'description': 'Educational garden for local schools',
                'address': '789 Mission St, San Francisco, CA',
                'latitude': 37.7649,
                'longitude': -122.4094,
                'created_by': {'get_full_name': lambda: 'Carol Davis'},
                'timeline': '3-6 months'
            }
        ]
        all_gardens = mock_gardens
    
    # Mock gardener data if no real user
    if not test_gardener:
        test_gardener = {
            'id': 1,
            'get_full_name': lambda: 'Test Gardener',
            'latitude': 37.7749,
            'longitude': -122.4194
        }
        
        # Mock gardener's gardens (subset of all gardens)
        gardener_gardens = mock_gardens[:2] if 'mock_gardens' in locals() else list(all_gardens)[:2]
    else:
        # Get real gardener's gardens
        gardener_gardens = Garden.objects.filter(
            created_by=test_gardener,
            latitude__isnull=False,
            longitude__isnull=False
        )
    
    context = {
        # For discover gardens map test
        'gardens': all_gardens,
        
        # For gardener profile map test  
        'gardener': test_gardener,
        'gardener_gardens': gardener_gardens,
        
        # Test scenarios
        'test_scenarios': [
            {
                'name': 'Discover Gardens Map',
                'description': 'Shows all gardens with search functionality',
                'gardens_count': len(all_gardens)
            },
            {
                'name': 'Gardener Profile Map',
                'description': 'Shows specific gardener\'s gardens and location',
                'gardens_count': len(gardener_gardens)
            }
        ]
    }
    
    return render(request, 'main_app/test_maps.html', context)

def start(request):
    return render(request, 'main_app/start.html')

# class UserUpdate(UpdateView):
#     model = User
#     form_class = UserForm
#     # reverse_lazy doesn't generate a URL immediately (ie 'lazily'). Used in particular in CBV success_urls
#     success_url = reverse_lazy('start')
    
#     # Update only the logged-in user.
#     def get_object(self):
#         return self.request.user

class GardenCreate(CreateView):
    model = Garden
    form_class = GardenForm
    success_url = '/profile/'
    
    # Adding this due to null error upon form submission. This makes sure to override the created_by relationship field and assign it automatically to the user. https://docs.djangoproject.com/en/5.2/topics/class-based-views/generic-editing/
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
