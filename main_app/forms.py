from django import forms
from .models import Garden, GoalOption, PlantOption, SupportOption, User


class GardenForm(forms.ModelForm):
    # Added these hidden fields for map coordinates
    latitude = forms.FloatField(widget=forms.HiddenInput(), required=False)
    longitude = forms.FloatField(widget=forms.HiddenInput(), required=False)
                                 
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
            'name',
            'address',
            'latitude',
            'longitude',
            'goals',
            'other_goal',
            'plants_to_grow',
            'support_needed',
            'timeline',
        ]
        widgets = {
            'timeline': forms.RadioSelect(attrs={'class': 'timeline-radio'}),
        }

# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = [
#             'experience',
#             # I get an error when I have this added noting that this is not a field that can be updated.
#             # https://stackoverflow.com/questions/62695029/fielderror-created-cannot-be-specified-for-post-model-form-as-it-is-a-non-edi
#             # 'location'
#         ]
#         widgets = {
#             'experience': forms.RadioSelect(attrs={'class': 'experience-radio'}),
#         }
