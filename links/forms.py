from django import forms
from .models import Link

class AdminLoginForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

class LinkForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ['short_id', 'destination']
