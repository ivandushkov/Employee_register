from django.core.validators import MaxLengthValidator, RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib import messages

from django.core.exceptions import ValidationError
import re
def validate_terms_agreement(value):
    if not value:
        raise ValidationError('You must agree to the terms and conditions.')


class User(AbstractUser):
    no_digits_validator = RegexValidator(r'^[A-Za-z]+$', "The text should contain only letters.")
    only_digits_validator = RegexValidator(r'^\d+$', "The phone number should only contain digits.")

    firstname = models.CharField(max_length=30, null=True, blank=True, validators=[MaxLengthValidator(30, message="Too many letters"), no_digits_validator])
    surname = models.CharField(max_length=30, null=True, blank=True, validators=[MaxLengthValidator(30, message="Too many letters"), no_digits_validator])
    lastname = models.CharField(max_length=40, null=True, blank=True, validators=[MaxLengthValidator(40, message="Too many letters"), no_digits_validator])
    avatar = models.ImageField(null=True, default="avatar.jpg")
    phone_number = models.CharField(max_length=12, null=True, blank=True, validators=[MaxLengthValidator(12, message="Have too many digits"), only_digits_validator])
    terms = models.BooleanField(default=False, validators=[validate_terms_agreement])

    def delete(self, *args, **kwargs):
        self.user.delete()
        super().delete(*args, **kwargs)

