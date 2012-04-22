from django import forms

from planning.models import Planning


class PlanningForm(forms.ModelForm):
    class Meta:
        model = Planning
        fields = ('profiles', 'lat', 'lon', 'radius')
