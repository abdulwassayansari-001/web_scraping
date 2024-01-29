from django import forms
from .models import *

class MembersForm(forms.ModelForm):
    class Meta:
        model = Members
        fields = '__all__' 


class CommitteesForm(forms.ModelForm):
    class Meta:
        model = Committees
        fields = '__all__'


class SubCommitteesForm(forms.ModelForm):
    class Meta:
        model = SubCommittees
        fields = '__all__'


class CSVMemberForm(forms.ModelForm):
    class Meta:
        model = Members
        fields = []


class CSVCommitteeForm(forms.ModelForm):
    class Meta:
        model = Committees
        fields = []


class CSVTitleForm(forms.ModelForm):
    class Meta:
        model = Title
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

    # Optionally, you can customize the __init__ method to further modify form behavior
    # def __init__(self, *args, **kwargs):
    #     super(DataForm, self).__init__(*args, **kwargs)
    #     # Additional customizations here
        








# class DataForm(forms.ModelForm):
#     committee = forms.ModelMultipleChoiceField(
#         queryset=Committees.objects.all(),
#         widget=forms.CheckboxSelectMultiple,
#         required=False
#     )
#     subcommittee = forms.ModelMultipleChoiceField(
#         queryset=SubCommittees.objects.all(),
#         widget=forms.CheckboxSelectMultiple,
#         required=False
#     )
#     hierarchy = forms.ModelMultipleChoiceField(
#         queryset=Hierarchy.objects.all(),
#         widget=forms.CheckboxSelectMultiple,
#         required=False
#     )
#     title = forms.ModelMultipleChoiceField(
#         queryset=Title.objects.all(),
#         widget=forms.CheckboxSelectMultiple,
#         required=False
#     )

#     class Meta:
#         model = Data
#         fields = ['member', 'committee', 'subcommittee', 'title', 'hierarchy']

#     # Optionally, you can customize the __init__ method to further modify form behavior
#     # def __init__(self, *args, **kwargs):
#     #     super(DataForm, self).__init__(*args, **kwargs)
#     #     # Additional customizations here