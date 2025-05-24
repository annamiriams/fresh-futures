from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models as gis_models
from django.db import models

class User(AbstractUser):
    """Custom User model with location fields"""
    # Django's built-in fields are inherited:
    # username, email, password, first_name, last_name, etc.
    
    # location fields:
    address = models.CharField(max_length=500, blank=True)
    latitude = models.FloatField(null=True, blank=True, editable=False)  # Hidden from users
    longitude = models.FloatField(null=True, blank=True, editable=False)  # Hidden from users
    location = gis_models.PointField(null=True, blank=True, editable=False)  # Hidden from users
    
    # custom save method to create geospatial data
    def save(self, *args, **kwargs):
        # automatically create Point from lat/lng
        if self.latitude and self.longitude:
            from django.contrib.gis.geos import Point
            self.location = Point(self.longitude, self.latitude)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.username

class Garden(models.Model):
    """Garden model with location fields"""
    # Basic garden information
    name = models.CharField(max_length=200)
    description = models.TextField()
    
    # Location fields
    address = models.CharField(max_length=500, blank=True)
    latitude = models.FloatField(null=True, blank=True, editable=False)  # Hidden from users
    longitude = models.FloatField(null=True, blank=True, editable=False)  # Hidden from users
    location = gis_models.PointField(null=True, blank=True, editable=False)  # Hidden from users
    
    # Relationships 
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        # automatically create Point from lat/lng
        if self.latitude and self.longitude:
            from django.contrib.gis.geos import Point
            self.location = Point(self.longitude, self.latitude)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


