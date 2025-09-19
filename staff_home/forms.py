from django import forms
from .models import Announcments,Resource,Question
from django.forms import DateTimeInput
import datetime
from .models import ProblemStatementConfig, ProblemStatementSection,Brochure, Submission, SubmissionWindow
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

        def clean_file(self):
            file = self.cleaned_data.get('file')
            max_size = 50 * 1024 * 1024  # 50 MB
            if file.size > max_size:
                raise forms.ValidationError("File too large (max 50 MB).")
            return file

class SubmissionWindowForm(forms.ModelForm):
    class Meta:
        model = SubmissionWindow
        fields = ["title", "description", "start_date", "end_date", "is_visible"]

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ["link"]

class TestForm(forms.ModelForm):
    class Meta:
        fields= [
             "title",
            "description",
            "code",
            "start_datetime",
            "end_datetime",
            "duration_minutes",
            "is_visible",
        ]
        widgets = {
            "start_datetime": DateTimeInput(attrs={"type": "datetime-local", "class": "form-control"}),
            "end_datetime": DateTimeInput(attrs={"type": "datetime-local", "class": "form-control"}),
            "duration_minutes": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "code": forms.TextInput(attrs={"class": "form-control"}),
            "is_visible": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = [
            "text",
            "question_type",      # e.g., MCQ, Descriptive, Coding
            "options",            # JSON/TextField for MCQs
            "correct_answer",     # For MCQ or coding expected output
            "marks",
            "negative_marks",
            "compiler_enabled",    # Boolean for coding questions
        ]
        widgets = {
            "text": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "question_type": forms.Select(attrs={"class": "form-select"}),
            "options": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "For MCQs: comma separated options"}),
            "correct_answer": forms.TextInput(attrs={"class": "form-control"}),
            "marks": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
            "negative_marks": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
            "compiler_enabled": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }