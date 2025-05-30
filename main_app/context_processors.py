# main_app/context_processors.py

# Context processors for Fresh Futures app
# These functions add variables to every template context automatically

from django.conf import settings

def mapbox_token(request):
    # Add Mapbox access token to all template contexts
    # This allows us to use {{ mapbox_token }} in any template
    
    return {
        'mapbox_token': getattr(settings, 'MAPBOX_ACCESS_TOKEN', '')
    }