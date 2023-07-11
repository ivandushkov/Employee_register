from django.contrib import admin
from .models import CompanyName
from account.models import User
from employees.models import Employees

admin.site.register(CompanyName)
admin.site.register(Employees)
admin.site.register(User)
