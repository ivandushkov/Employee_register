from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DeleteView, UpdateView, View, CreateView, TemplateView, DetailView

from .form import RegisterForm, UserForm, UserPasswordChange, PasswordResetForm_main
from .models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.views import LoginView, PasswordChangeView


def logout_page(request):
    logout(request)
    messages.add_message(request, messages.INFO, 'You successfully logged out')
    return redirect('login')


class RegisterAccount(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = '/login/'

    def form_valid(self, form):
        if User.objects.filter(username=self.request.POST['username']).exists():  # Username is already taken
            return self.form_invalid(form)
        if self.request.POST['terms'] != "on":
            return self.form_invalid(form)
        form.save()
        messages.success(self.request, "Great! Registration is Done.")
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.POST.get('terms') != "on":
            messages.error(self.request, "Please agree the terms.")
        return super().form_invalid(form)


class LoginAccount(LoginView):
    template_name = 'login.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = authenticate(self.request, username=self.request.POST.get('username'), password=self.request.POST.get('password'))
        if user is not None:
            if self.request.POST.get('remember') == "on":
                self.request.session.set_expiry(2592000)  # save session for 30 days
            login(self.request, user)
            return redirect(self.success_url)
        else:
            return self.form_invalid()

    def form_invalid(self, form):
        messages.error(self.request, "Wrong username or password")
        return super().form_invalid(form)


@method_decorator(login_required(login_url='login'), name='dispatch')
class UpdateAccount(UpdateView):
    model = User
    form_class = UserForm
    template_name = 'profile.html'
    success_url = reverse_lazy('profile')  # Replace 'profile' with the appropriate URL name

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Profile is updated')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Cannot update profile')
        return super().form_invalid(form)


@method_decorator(login_required(login_url='login'), name='dispatch')
class ChangePasswordAccount(PasswordChangeView):
    template_name = 'change_password.html'
    form_class = UserPasswordChange


@method_decorator(login_required(login_url='login'), name='dispatch')
class DeleteAccount(DeleteView):
    model = User
    template_name = 'delete_profile.html'
    form_class = UserForm
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        return self.request.user

    def post(self, request, *args, **kwargs):
        user = self.model.objects.filter(username=self.request.user.username)
        if user is not None:
            user.delete()
            messages.success(request, "Account is deleted")
            return redirect(self.success_url)
        return redirect(self.success_url)


class PasswordResetView_main(PasswordResetView):
    form_class = PasswordResetForm_main


