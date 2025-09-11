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
    
    def clean_payment_screenshot(self):
        file = self.cleaned_data.get("payment_screenshot")
        if file:
            if not file.name.lower().endswith(".png"):
                raise forms.ValidationError("Only .png files are allowed for payment proof.")
        return file