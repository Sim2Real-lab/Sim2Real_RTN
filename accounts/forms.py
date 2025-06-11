from django import forms

class OTPRequestForm(forms.Form):
    email = forms.EmailField()

class OTPVerifyForm(forms.Form):
    email = forms.EmailField()
    otp = forms.CharField(max_length=6)
    new_password1 = forms.CharField(widget=forms.PasswordInput)
    new_password2 = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('Enter New Password')
        p2 = cleaned_data.get('Confirm Password')
        if p1 != p2:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data
