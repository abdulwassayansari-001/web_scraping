from django import forms

class RequestNewVerificationEmail(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        })
    )

    def __init__(self, *args, **kwargs):
        super(RequestNewVerificationEmail, self).__init__(*args, **kwargs)
        self.fields['email'].label = ''
