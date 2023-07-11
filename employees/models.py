from django.db import models
from base.models import CompanyName
from django.core.validators import RegexValidator, MaxLengthValidator


class JobPositionChoices:
    SYSTEM_ADMINISTRATOR = 'SA'
    WEB_DEVELOPER = 'WD'
    DEVOPS = 'DO'
    BACKEND_DEVELOPER = 'BE'
    CYBER_SECURITY = 'CS'
    NETWORK_ADMINISTRATOR = 'NA'

    CHOICES = [
        (SYSTEM_ADMINISTRATOR, 'System Administrator'),
        (WEB_DEVELOPER, 'Web Developer'),
        (DEVOPS, 'DevOps'),
        (BACKEND_DEVELOPER, 'Backend Developer'),
        (CYBER_SECURITY, 'Cyber Security'),
        (NETWORK_ADMINISTRATOR, "Network Administrator"),
    ]


class Employees(models.Model):
    no_digits_validator = RegexValidator(r'^[A-Za-z]+$', "The text should contain only letters.")
    only_digits_validator = RegexValidator(r'^\d+$', "The phone number should only contain digits.")

    firstname = models.CharField(max_length=30,
                                 validators=[MaxLengthValidator(30, message="Too many letters"), no_digits_validator])
    surname = models.CharField(max_length=30,
                               validators=[MaxLengthValidator(30, message="Too many letters"), no_digits_validator])
    lastname = models.CharField(max_length=30,
                                validators=[MaxLengthValidator(30, message="Too many letters"), no_digits_validator])
    phone = models.CharField(max_length=12,
                             validators=[MaxLengthValidator(12, message="Too many digits"), only_digits_validator])
    address = models.CharField(max_length=100, validators=[MaxLengthValidator])
    job_position = models.CharField(max_length=2, choices=JobPositionChoices.CHOICES)
    skills = models.TextField(max_length=500, validators=[MaxLengthValidator(500, message="You reach max length")])
    company_name = models.ForeignKey(CompanyName, on_delete=models.SET_NULL, null=True, related_name='companies')
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return f"{self.firstname} {self.surname} {self.lastname}"
