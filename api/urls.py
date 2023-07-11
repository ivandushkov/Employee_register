from django.urls import path
from . import views


urlpatterns = [
    path('', views.routes),
    path('employees/', views.get_employees),
    path('employee/<int:id>', views.get_employee)
]
