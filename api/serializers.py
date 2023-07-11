import rest_framework.serializers
from rest_framework.serializers import ModelSerializer
from employees.models import Employees


class EmployeeSerializer(ModelSerializer):
    image = rest_framework.serializers.ImageField

    class Meta:
        model = Employees
        fields = '__all__'