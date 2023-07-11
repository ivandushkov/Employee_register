from django.forms import ModelForm
from base.models import CompanyName
from .models import Employees
from django import forms


class EmployeeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user_id', None) # get user_id = owner
        super().__init__(*args, **kwargs)
        #companies = CompanyName.objects.filter(company_owner=username)
        #self.fields['company_name'].choices = [(company.id, company.company_name) for company in companies]
        self.fields['company_name'].queryset = CompanyName.objects.filter(company_owner=user_id)

    class Meta:
        model = Employees
        ordering = ['firstname']
        fields = '__all__'
        widgets = {
            'firstname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Firstname'}),
            'surname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Surname'}),
            'lastname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lastname'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'job_position': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Job position'}),
            'skills': forms.Textarea(
                attrs={'class': 'form-control', 'rows': '3', 'placeholder': 'Skills (description)'}
            ),
            'company_name': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Select company'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file', 'type': 'file'}),
        }