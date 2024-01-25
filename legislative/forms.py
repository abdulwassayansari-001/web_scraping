from django import forms
from .models import Members, Committees, SubCommittees, Data

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



class DataForm(forms.ModelForm):
    class Meta:
        model = Data
        fields = "__all__"