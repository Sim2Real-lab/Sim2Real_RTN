from django import forms
from .models import Team

class TeamCreationForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name']

class JoinCodeForm(forms.Form):
    join_code = forms.UUIDField(label="Join Code :")


class PaymentProofForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['payment_ref', 'payment_screenshot']
        widgets = {
            'payment_ref': forms.TextInput(attrs={'placeholder': 'Enter UPI Reference Number'}),
        }