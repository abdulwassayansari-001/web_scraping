# forms.py
from django import forms
from .models import DataScrap, Feedback

class CSVUploadForm(forms.ModelForm):
    class Meta:
        model = DataScrap
        fields = []  # Empty fields to only allow file upload

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['feedback_data', ]