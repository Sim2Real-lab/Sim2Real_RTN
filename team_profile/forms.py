from django import forms
from .models import Team

class TeamCreationForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name']

class JoinCodeForm(forms.Form):
    join_code = forms.UUIDField(label="Join Code :")
