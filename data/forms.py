# forms.py
from django import forms
from .models import DataScrap, DataScrapImages

class CSVUploadForm(forms.ModelForm):
    class Meta:
        model = DataScrap
        fields = []  # Empty fields to only allow file upload

class ImageUploadForm(forms.ModelForm):
    zip_file = forms.FileField(label="ZIP File", required=False, widget=forms.ClearableFileInput(attrs={'accept': '.zip'}))

    class Meta:
        model = DataScrapImages
        fields = []
