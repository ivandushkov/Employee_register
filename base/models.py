from django.db import models
from account.models import User


class CompanyName(models.Model):
    company_name = models.CharField(unique=True, max_length=60, help_text="Company name must be unique")
    company_owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.company_name



