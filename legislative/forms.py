from django import forms
from .models import *


class CSVMemberForm(forms.ModelForm):
    class Meta:
        model = Members
        fields = []


class CSVCommitteeForm(forms.ModelForm):
    class Meta:
        model = Committees
        fields = []

class CSVSubCommitteeForm(forms.ModelForm):
    class Meta:
        model = Committees
        fields = []


class CSVTitleForm(forms.ModelForm):
    class Meta:
        model = Title
        fields = []


class CSVHierarchyForm(forms.ModelForm):
    class Meta:
        model = Hierarchy
        fields = []


class DataForm(forms.ModelForm):
    class Meta:
        model = Data
        fields = ['member', 'committee', 'subcommittee', 'title', 'hierarchy']
        widgets = {
            'member': forms.Select(attrs={'class': 'dropdown-field'}),
            'committee': forms.Select(attrs={'class': 'dropdown-field'}),
            'subcommittee': forms.Select(attrs={'class': 'dropdown-field'}),
            'title': forms.Select(attrs={'class': 'dropdown-field'}),
            'hierarchy': forms.Select(attrs={'class': 'dropdown-field'}),
        }