# forms.py
from django import forms
from .models import DataScrap, DataScrapImages

class CSVUploadForm(forms.ModelForm):
    class Meta:
        model = DataScrap
        fields = []  # Empty fields to only allow file upload

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = DataScrapImages
        fields = ['image']
