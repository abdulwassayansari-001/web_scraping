# forms.py
from django import forms
from .models import DataScrap

class CSVUploadForm(forms.ModelForm):
    class Meta:
        model = DataScrap
        fields = []  # Empty fields to only allow file upload
