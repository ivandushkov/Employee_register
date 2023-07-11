from . import views
from django.conf import settings
from django.urls import path
from django.conf.urls.static import static

urlpatterns = [
    path("employee/", views.AddEmployee.as_view(), name="employee"),
    path("search/", views.SearchEmployee.as_view(), name="search"),
    path('delete_employee/<int:pk>/', views.DeleteEmployee.as_view(), name='delete_employee'),
    path("edit/<int:pk>/", views.EditEmployee.as_view(), name="edit"),

    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)