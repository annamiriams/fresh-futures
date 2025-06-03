# main_app/context_processors.py

# Context processors for Fresh Futures app
# These functions add variables to every template context automatically

from django.conf import settings
import os

def mapbox_token(request):
    token = getattr(settings, 'MAPBOX_ACCESS_TOKEN', '')
    print(f"DEBUG: Context processor token = {token}")
    print(f"DEBUG: Raw env var = {os.getenv('MAPBOX_ACCESS_TOKEN')}")
    
    return {
        'mapbox_token': token
    }