from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import UpdateView, DeleteView, CreateView, DetailView, ListView

from base.models import CompanyName
from .form import EmployeeForm
from .models import Employees, JobPositionChoices
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages

# Create your views here.


@method_decorator(login_required(login_url='login'), name='dispatch')
class AddEmployee(CreateView):
    template_name = 'employee.html'
    form_class = EmployeeForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user_id'] = self.request.user.id
        return kwargs

    def form_valid(self, form):
        form.save()
        messages.success(self.request, f'You successfully registered employee: {form.cleaned_data["firstname"]} {form.cleaned_data["surname"]} {form.cleaned_data["lastname"]}')
        return redirect('employee')

    def form_invalid(self, form):
        messages.error(self.request, "Can't register this employee")
        return redirect('employee')


@method_decorator(login_required(login_url='login'), name='dispatch')
class SearchEmployee(ListView):
    model = Employees
    template_name = 'search.html'
    form_class = EmployeeForm
    paginate_by = 6
    context_object_name = 'employees'

    def get_queryset(self):
        queryset = Employees.objects.filter(company_name__company_owner=self.request.user.id)
        q = self.request.GET.get('q')
        job_position = self.request.GET.get('job_position')

        if q:
            names = q.split()
            if len(names) > 1:
                queryset = queryset.filter(
                    Q(firstname__icontains=names[0]) & Q(lastname__icontains=names[1])
                )
            else:
                queryset = queryset.filter(
                    Q(firstname__icontains=names[0]) | Q(lastname__icontains=names[0])
                )
                self.paginate_by = queryset.count()

        if job_position:
            queryset = queryset.filter(job_position=job_position)
            self.paginate_by = queryset.count()

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        q = self.request.GET.get('q', '')
        job_position = self.request.GET.get('job_position')

        context['total_count'] = self.model.objects.filter(company_name__company_owner=self.request.user.id).count()
        context['q'] = q
        context['job_position'] = job_position
        context['JobPositionChoices'] = JobPositionChoices.CHOICES

        return context


@method_decorator(login_required(login_url='login'), name='dispatch')
class EditEmployee(UpdateView):
    model = Employees
    template_name = 'edit.html'
    form_class = EmployeeForm
    success_url = '/search/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        employee = self.get_object()
        context['image'] = employee.image
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user_id'] = self.request.user.id
        return kwargs

    def form_valid(self, form):
        if self.request.POST['firstname'] == 'admin':
            return self.form_invalid(form)
        messages.success(self.request, 'Employee is updated successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Can`t update employee data')
        return super().form_invalid(form)


@method_decorator(login_required(login_url='login'), name='dispatch')
class DeleteEmployee(DeleteView):
    model = Employees
    success_url = '/search/'

    def get(self, request, *args, **kwargs):
        try:
            employee = self.get_object()
            if request.user.username == str(employee.company_name.company_owner):
                employee.delete()
                messages.success(request, f'You successfully delete employee: {employee.firstname} {employee.surname} {employee.lastname}')
                return redirect('search')
        except employee.DoesNotExist:
            messages.error(request, "Employee not found")
            return redirect('search')

















# @login_required(login_url='/login')
# def add_employee(request):
#     form = EmployeeForm(username=request.user.id)
#     if request.method == 'POST':
#         form = EmployeeForm(request.POST, request.FILES, username=request.user.id)
#         try:
#             if form.is_valid():
#                 employee = form.save(commit=False)
#                 employee.image = request.FILES.get('image')
#                 employee.save()  # Save the employee instance with the uploaded image
#                 messages.success(request, f'You successfully registered employee: {employee.firstname} {employee.surname} {employee.lastname}')
#                 return redirect('employee')
#         except ValueError:
#             messages.error("Can`t register this employee")
#             return redirect('employee')
#     return render(request, 'employee.html', {'form': form})

#@login_required(login_url='/login')
# def search_employee(request):
#     queryset = Employees.objects.filter(company_name__company_owner=request.user.id)
#     items_per_page = 3
#     paginator = Paginator(queryset, items_per_page)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     objects = page_obj.object_list
#
#     q = request.GET.get('q', '')
#     job_position = request.GET.get('job_position')
#     print(job_position)
#     employees_list = None
#     if q == '':
#         employees_list = Employees.objects.filter(company_name__company_owner=request.user.id)[:3]
#
#     employees = Employees.objects.filter(company_name__company_owner=request.user.id).filter(
#         Q(firstname__icontains=q) | Q(lastname__icontains=q))
#
#     if job_position is None:
#         filtered_employees = None
#     else:
#         filtered_employees = employees.filter(job_position=job_position)
#
#     context = {
#         'employees': employees,
#         'employees_list': employees_list,
#         'page_obj': page_obj,
#         'objects': objects,
#         'job_position': job_position,
#         'filtered_employees': filtered_employees,
#         'JobPositionChoices': JobPositionChoices.CHOICES,
#     }
#
#     return render(request, 'search.html', context)