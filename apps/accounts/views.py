from django.shortcuts import redirect
from django.contrib.auth.views import (
    LoginView, PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView
)
from django.contrib.auth import logout
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, View
from .forms import LoginForm, RegisterForm
from .models import User
import logging

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.views import LoginView, LogoutView
from .models import User
from .forms import EmployeeCreateForm, EmployeeUpdateForm, EmployeeSearchForm, LoginForm, RegisterForm

logger = logging.getLogger(__name__)


class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user
        # Adapte selon tes règles de rôles
        if hasattr(user, 'is_admin') and user.is_admin():
            return reverse_lazy('core:dashboard')
        return reverse_lazy('core:caisse')


class UserRegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Compte créé avec succès, vous pouvez vous connecter.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Erreur dans le formulaire, vérifiez vos informations.")
        return super().form_invalid(form)


class UserLogoutView(View):
    def get(self, request, *args, **kwargs):
        return self.logout_user(request)
    def post(self, request, *args, **kwargs):
        return self.logout_user(request)
    def logout_user(self, request):
        logout(request)
        messages.success(request, "Vous êtes bien déconnecté.")
        return redirect('accounts:login')


# ---------------------- MOT DE PASSE OUBLIÉ ------------------------

class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('accounts:password_reset_done')

    def form_valid(self, form):
        messages.success(self.request, "Un email de réinitialisation a été envoyé, vérifiez vos mails & spams.")
        return super().form_valid(form)


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'

# Alias (important en cas d'import sauvage)
PasswordResetView = CustomPasswordResetView
PasswordResetDoneView = CustomPasswordResetDoneView
PasswordResetConfirmView = CustomPasswordResetConfirmView
PasswordResetCompleteView = CustomPasswordResetCompleteView


# Mixin pour restreindre aux admins
class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin()
    def handle_no_permission(self):
        messages.error(self.request, "Accès refusé : administrateurs uniquement.")
        return redirect('accounts:login')
# ====================== CRUD EMPLOYÉS ======================
class EmployeeListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = User
    template_name = 'accounts/employees/employee_list.html'
    context_object_name = 'employees'
    paginate_by = 15

    def get_queryset(self):
        qs = User.objects.exclude(pk=self.request.user.pk).order_by('-date_joined')
        form = EmployeeSearchForm(self.request.GET)
        if form.is_valid():
            search = form.cleaned_data.get('search')
            role = form.cleaned_data.get('role')
            status = form.cleaned_data.get('status')
            if search:
                qs = qs.filter(first_name__icontains=search) \
                     | qs.filter(last_name__icontains=search) \
                     | qs.filter(email__icontains=search)
            if role: qs = qs.filter(role=role)
            if status=='active': qs = qs.filter(is_active=True)
            elif status=='inactive': qs = qs.filter(is_active=False)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['search_form'] = EmployeeSearchForm(self.request.GET)
        ctx['total'] = self.get_queryset().count()
        ctx['active'] = self.get_queryset().filter(is_active=True).count()
        ctx['inactive'] = self.get_queryset().filter(is_active=False).count()
        return ctx

class EmployeeCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = User
    form_class = EmployeeCreateForm
    template_name = 'accounts/employees/employee_form.html'
    success_url = reverse_lazy('accounts:employee_list')
    def form_valid(self, form):
        resp = super().form_valid(form)
        messages.success(self.request, f"Employé {self.object.get_full_name()} créé !")
        return resp

class EmployeeUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = User
    form_class = EmployeeUpdateForm
    template_name = 'accounts/employees/employee_form.html'
    success_url = reverse_lazy('accounts:employee_list')
    def get_queryset(self):
        return User.objects.exclude(pk=self.request.user.pk)  ##### empêche auto-modification
    def form_valid(self, form):
        resp = super().form_valid(form)
        messages.success(self.request, f"Employé {self.object.get_full_name()} mis à jour !")
        return resp

class EmployeeDetailView(LoginRequiredMixin, AdminRequiredMixin, DetailView):
    model = User
    template_name = 'accounts/employees/employee_detail.html'
    context_object_name = 'employee'
    def get_queryset(self):
        return User.objects.exclude(pk=self.request.user.pk)

class EmployeeDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = User
    template_name = 'accounts/employees/employee_confirm_delete.html'
    success_url = reverse_lazy('accounts:employee_list')
    def get_queryset(self):
        return User.objects.exclude(pk=self.request.user.pk)
    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(request, f"Employé {obj.get_full_name()} supprimé.")
        return super().delete(request, *args, **kwargs)

class EmployeeToggleStatusView(LoginRequiredMixin, AdminRequiredMixin, View):
    def post(self, request, pk):
        emp = get_object_or_404(User, pk=pk)
        if emp.pk == request.user.pk:
            return JsonResponse({'success': False, 'msg': "Vous ne pouvez pas désactiver vous-même."})
        emp.is_active = not emp.is_active
        emp.save()
        state = 'activé' if emp.is_active else 'désactivé'
        return JsonResponse({'success': True, 'state': state})