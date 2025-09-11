from django import forms
from .models import Announcments,Resource
import datetime
from .models import ProblemStatementConfig, ProblemStatementSection,Brochure
class AnnouncmentForm(forms.ModelForm):
    class Meta:
        model=Announcments
        fields=[
            'message',
            'schedule_for_later',
            'valid_till',
            'manual_visibility',
            'manual_validity',
            'category',
        ]

        widgets={
            'schedule_for_later': forms.DateInput(attrs={'type': 'date'}),
            'valid_till': forms.DateInput(attrs={'type': 'date'}),
        }

        def clean(self):
            cleaned_data = super().clean()
            schedule_date = cleaned_data.get('schedule_for_later')
            valid_till = cleaned_data.get('valid_till')
            today = datetime.date.today()

        # Validate: schedule_for_later can't be in the past
            if schedule_date and schedule_date < today:
                self.add_error('schedule_for_later', 'Scheduled date cannot be in the past.')

        # Validate: valid_till must be after schedule_for_later
            if valid_till and schedule_date and valid_till < schedule_date:
                self.add_error('valid_till', 'Valid till date must be after the scheduled date.')

            return cleaned_data
        

class ProblemStatementConfigForm(forms.ModelForm):
    class Meta:
        model = ProblemStatementConfig
        fields = ["enabled", "file"]

class ProblemStatementSectionForm(forms.ModelForm):
    class Meta:
        model = ProblemStatementSection
        fields = ["title", "content", "order"]

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ["title", "file", "link"]

class BrochureForm(forms.ModelForm):
    class Meta:
        model = Brochure
        fields = ["file"]
