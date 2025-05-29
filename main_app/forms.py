from django import forms
from .models import Garden, GoalOption, PlantOption, SupportOption

class GardenForm(forms.ModelForm):
    goals = forms.ModelMultipleChoiceField(
        # queryset => collection of db rows
        # Each option from this queryset will become a checkbox option (from GoalOption.objects.all()) 
        queryset=GoalOption.objects.all().order_by('name'),
            # Could change how these options are ordered but for now they're alphabetical.
        widget=forms.CheckboxSelectMultiple,
            # Changes the default usage of dropdown options to multi-select boxes. 
        required=False
    )
    plants_to_grow = forms.ModelMultipleChoiceField(
        queryset=PlantOption.objects.all().order_by('name'),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    support_needed = forms.ModelMultipleChoiceField(
        queryset=SupportOption.objects.all().order_by('name'),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Garden
        fields = [
            'address',
            'goals', 
            'other_goal', 
            'plants_to_grow', 
            'support_needed', 
            'timeline',
        ] 
        
