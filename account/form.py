from django import forms

from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, PasswordResetForm
from base.models import User
import re
from django.core.exceptions import ValidationError


def validate_password(value):
    pattern = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*()_\-+=.]).{8,}$"
    if not re.match(pattern, value):
        raise forms.ValidationError(
            "Password must contain at least 8 characters, including one digit, one lowercase letter, one uppercase letter, and one special character (!@#.$%^&*()_-+=)."
        )


class RegisterForm(UserCreationForm):
    username = forms.CharField(label="", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Enter username"}))
    email = forms.CharField(label="", max_length=60,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Enter email"}))
    password1 = forms.CharField(label="", max_length=32, widget=forms.TextInput(
        attrs={'class': 'form-control', 'type': 'password', 'placeholder': "Enter password"}),
                                validators=[validate_password])
    password2 = forms.CharField(label="", max_length=32, widget=forms.TextInput(
        attrs={'class': 'form-control', 'type': 'password', 'placeholder': "Retype password"}))
    terms = forms.BooleanField(label="Agree with the terms:")

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "terms"]


class UserForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['firstname'].required = False
        self.fields['surname'].required = False
        self.fields['lastname'].required = False
        self.fields['phone_number'].required = False
        self.fields['email'].required = False

    class Meta:
        model = User
        fields = ['firstname', 'lastname', 'surname', 'phone_number', 'email', 'avatar']
        widgets = {
            'firstname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Firstname'}),
            'surname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Surname'}),
            'lastname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lastname'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control-file', 'type': 'file'}),
        }


class UserPasswordChange(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].required = False
        self.fields['new_password2'].required = False
        self.fields['old_password'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Current Password'})
        self.fields['new_password1'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'New Password'})
        self.fields['new_password2'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Confirm New Password'})

    class Meta:
        model = User
        fields = []

    def clean_new_password1(self):
        new_password1 = self.cleaned_data.get('new_password1')
        if len(new_password1) < 8:
            raise ValidationError('Password must be at least 8 characters long.')
        return new_password1


class PasswordResetForm_main(PasswordResetForm):
    email = forms.EmailField(
        label = ("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'class': 'form-control', "autocomplete": "email"}),
    )
