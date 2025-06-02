from django.contrib import admin

# Register your models here.
from .models import User, GoalOption, PlantOption, SupportOption, Garden
admin.site.register(User)
admin.site.register(GoalOption)
admin.site.register(PlantOption)
admin.site.register(SupportOption)
admin.site.register(Garden)