from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models as gis_models
from django.db import models

class User(AbstractUser):
    """Custom User model with location fields"""
    # Django's built-in fields are inherited:
    # username, email, password, first_name, last_name, etc.
    
    # Adding so we can integrate the user survey into the register survey.
    has_completed_onboarding = models.BooleanField(default=False)
    
    EXPERIENCE_LEVEL = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('expert', 'Expert'),
    ]
    experience = models.CharField(max_length=12, choices=EXPERIENCE_LEVEL, default='beginner')
    
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
        # Return a string representation of the user (in admin panel, etc.)
        return self.first_name + ' ' + self.last_name

class GoalOption(models.Model):
    name = models.CharField(max_length=100, unique=True)
        # unique=True ensures there aren't duplicate goals options

    def __str__(self):
        return self.name
    
class PlantOption(models.Model):
    name = models.CharField(max_length=100, unique=True)
        # unique=True ensures there aren't duplicate plant options
    
    def __str__(self):
        return self.name
    
class SupportOption(models.Model):
    name = models.CharField(max_length=100, unique=True)
        # unique=True ensures there aren't duplicate support options

    def __str__(self):
        return self.name

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
    
    # Survey fields
        # Create a ManyToMany relationship between Garden and the three survey questions (GardenGoals, PlantPlans, SupportNeeded)
            # E.g.: A garden can have multiple goals, and one goal can be associated with multiple gardens
        # blank=True allows a garden to leave any of these questions blank
    goals = models.ManyToManyField(GoalOption, blank=True, help_text='Select your goals for this garden.')
    other_goal = models.TextField(blank=True, help_text='Is your goal not listed? Add it here!')
    plants_to_grow = models.ManyToManyField(PlantOption, blank=True, help_text='Select what you\'d like to grow in your garden.')
    # other_plants ? Checking with UI team to see if they want this added.
    support_needed = models.ManyToManyField(SupportOption, blank=True, help_text='Select what kind of support you\'ll need.')
    # other_support ? Checking with UI team to see if they want this added.

    # Add some kind of free text field to address the question in the survey that currently reads "Are there others you might want to help?..."
    
    TIMELINE = [
        ('within 1 month', 'Within 1 Month'),
        ('1-3 months', '1-3 Months'),
        ('3-6 months', '3-6 Months'),
    ]
    timeline = models.CharField(max_length=14, choices=TIMELINE, default='within 1 month', help_text='How soon are you hoping to get started?')
    
    def save(self, *args, **kwargs):
        # automatically create Point from lat/lng
        if self.latitude and self.longitude:
            from django.contrib.gis.geos import Point
            self.location = Point(self.longitude, self.latitude)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


