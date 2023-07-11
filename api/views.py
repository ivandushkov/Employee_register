from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from employees.models import Employees
from .serializers import EmployeeSerializer


@api_view(['GET'])
def routes(request):
    routes = [
        'GET /api/employees',
        'GET /api/employee/1'
    ]
    return Response(routes)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_employee(request, id):
    try:
        employee = Employees.objects.get(pk=id)
        serializer = EmployeeSerializer(employee, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Employees.DoesNotExist:
        return Response({"Employee": "Not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def get_employees(request):
    if request.method == "POST":
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    try:
        employees = Employees.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except employees.DoesNotExist:
        return Response({"Employees": "No employees yet"})


