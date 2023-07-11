from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, View, CreateView, FormView
from .form import CompanyForm
from .models import CompanyName
from account.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def handle_404(request, exception):
    return render(request, '404.html', status=404)


@method_decorator(login_required(login_url='login'), name='dispatch')
class HomePage(FormView):
    template_name = 'home.html'
    form_class = CompanyForm
    success_url = '/home/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        companies = CompanyName.objects.filter(company_owner=self.request.user.id)
        context['companies'] = companies
        return context

    def form_valid(self, form):
        company_owner = self.request.user.username
        company_name = form.cleaned_data['company_name']
        owner = User.objects.get(username=company_owner)
        if CompanyName.objects.filter(company_name=company_name).exists():
            return self.form_invalid(form)
        else:
            new_company = CompanyName(company_name=company_name, company_owner=owner)
            new_company.save()
            messages.success(self.request, 'Your company has been successfully registered')
            return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Cannot duplicate company name')
        return super().form_invalid(form)






