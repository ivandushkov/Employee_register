from django import forms
from .models import CompanyName


class CompanyForm(forms.Form):
    company_name = forms.CharField(label="", max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Register your Company here....'}))

    class Meta:
        model = CompanyName
        fields = ['company_name', 'company_owner']
