# apps/accounts/views.py

import logging
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.views.generic import (
    View, ListView, CreateView, UpdateView, DetailView, DeleteView
)
from django.contrib.auth.views import (
    LoginView, PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import logout

from .models import User
from .forms import (
    LoginForm, RegisterForm,
    EmployeeCreateForm, EmployeeUpdateForm, EmployeeSearchForm,
    SupplierCreateForm, SupplierSearchForm,
    CategoryCreateForm, CategorySearchForm,
    ProductCreateForm, ProductSearchForm
)
from apps.core.models import Supplier, Category, Product

logger = logging.getLogger(__name__)


class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user
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
        logout(request)
        messages.success(request, "Vous êtes bien déconnecté.")
        return redirect('accounts:login')


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


# Alias
PasswordResetView = CustomPasswordResetView
PasswordResetDoneView = CustomPasswordResetDoneView
PasswordResetConfirmView = CustomPasswordResetConfirmView
PasswordResetCompleteView = CustomPasswordResetCompleteView


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
                qs = qs.filter(first_name__icontains=search) | qs.filter(last_name__icontains=search) | qs.filter(email__icontains=search)
            if role:
                qs = qs.filter(role=role)
            if status == 'active':
                qs = qs.filter(is_active=True)
            elif status == 'inactive':
                qs = qs.filter(is_active=False)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        form = EmployeeSearchForm(self.request.GET)
        qs = self.get_queryset()
        ctx['search_form'] = form
        ctx['total'] = qs.count()
        ctx['active'] = qs.filter(is_active=True).count()
        ctx['inactive'] = qs.filter(is_active=False).count()
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
        return User.objects.exclude(pk=self.request.user.pk)

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
        messages.success(request, f"Employé {obj.get_full_name()} supprimé !")
        return super().delete(request, *args, **kwargs)


class EmployeeToggleStatusView(LoginRequiredMixin, AdminRequiredMixin, View):
    def post(self, request, pk):
        emp = get_object_or_404(User, pk=pk)
        if emp.pk == request.user.pk:
            return JsonResponse({'success': False, 'msg': "Vous ne pouvez pas vous désactiver vous-même."})
        emp.is_active = not emp.is_active
        emp.save()
        state = 'activé' if emp.is_active else 'désactivé'
        return JsonResponse({'success': True, 'state': state})


# ====================== CRUD FOURNISSEURS ======================

import logging
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .forms import SupplierCreateForm, SupplierSearchForm
from apps.core.models import Supplier

logger = logging.getLogger(__name__)

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin()
    def handle_no_permission(self):
        messages.error(self.request, "Accès refusé : administrateurs uniquement.")
        return redirect('accounts:login')

class SupplierListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Supplier
    template_name = 'accounts/suppliers/supplier_list.html'
    context_object_name = 'suppliers'
    paginate_by = 15

    def get_queryset(self):
        qs = Supplier.objects.all().order_by('-created_at')
        form = SupplierSearchForm(self.request.GET)
        if form.is_valid():
            search = form.cleaned_data.get('search', '')
            status = form.cleaned_data.get('status', '')
            if search:
                qs = qs.filter(name__icontains=search)
            if status:
                qs = qs.filter(status=status)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        form = SupplierSearchForm(self.request.GET)
        qs = self.get_queryset()

        # Valeurs GET
        search_val = self.request.GET.get('search', '')
        status_val = self.request.GET.get('status', '')
        if form.is_valid():
            search_val = form.cleaned_data.get('search', '') or ''
            status_val = form.cleaned_data.get('status', '') or ''

        ctx.update({
            'search_form': form,
            'search_filter': search_val,
            'status_choices': Supplier.Status.choices,
            'status_filter': status_val,
            'total': qs.count(),
            'active': qs.filter(status=Supplier.Status.ACTIVE).count(),
            'inactive': qs.filter(status=Supplier.Status.INACTIVE).count(),
            'suspended': qs.filter(status=Supplier.Status.SUSPENDED).count(),
        })
        return ctx

class SupplierCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Supplier
    form_class = SupplierCreateForm
    template_name = 'accounts/suppliers/supplier_form.html'
    success_url = reverse_lazy('accounts:supplier_list')

    def form_valid(self, form):
        messages.success(self.request, f"Fournisseur {form.instance.name} créé !")
        return super().form_valid(form)

class SupplierUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Supplier
    form_class = SupplierCreateForm
    template_name = 'accounts/suppliers/supplier_form.html'
    success_url = reverse_lazy('accounts:supplier_list')

    def form_valid(self, form):
        messages.success(self.request, f"Fournisseur {form.instance.name} mis à jour !")
        return super().form_valid(form)

class SupplierDetailView(LoginRequiredMixin, AdminRequiredMixin, DetailView):
    model = Supplier
    template_name = 'accounts/suppliers/supplier_detail.html'
    context_object_name = 'supplier'

class SupplierDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Supplier
    template_name = 'accounts/suppliers/supplier_confirm_delete.html'
    success_url = reverse_lazy('accounts:supplier_list')

    def delete(self, request, *args, **kwargs):
        name = self.get_object().name
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f"Fournisseur {name} supprimé !")
        return response


# ====================== CRUD CATÉGORIES ======================

class CategoryListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Category
    template_name = 'accounts/categories/category_list.html'
    context_object_name = 'categories'
    paginate_by = 15

    def get_queryset(self):
        qs = Category.objects.all().order_by('name')
        form = CategorySearchForm(self.request.GET)
        if form.is_valid():
            search = form.cleaned_data.get('search')
            if search:
                qs = qs.filter(name__icontains=search)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        form = CategorySearchForm(self.request.GET)
        qs = self.get_queryset()
        ctx['search_form'] = form
        ctx['total'] = qs.count()
        return ctx


class CategoryCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Category
    form_class = CategoryCreateForm
    template_name = 'accounts/categories/category_form.html'
    success_url = reverse_lazy('accounts:category_list')

    def form_valid(self, form):
        messages.success(self.request, f"Catégorie '{form.instance.name}' créée !")
        return super().form_valid(form)


class CategoryUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryCreateForm
    template_name = 'accounts/categories/category_form.html'
    success_url = reverse_lazy('accounts:category_list')

    def form_valid(self, form):
        messages.success(self.request, f"Catégorie '{form.instance.name}' mise à jour !")
        return super().form_valid(form)


class CategoryDetailView(LoginRequiredMixin, AdminRequiredMixin, DetailView):
    model = Category
    template_name = 'accounts/categories/category_detail.html'
    context_object_name = 'category'


class CategoryDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Category
    template_name = 'accounts/categories/category_confirm_delete.html'
    success_url = reverse_lazy('accounts:category_list')

    def delete(self, request, *args, **kwargs):
        name = self.get_object().name
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f"Catégorie '{name}' supprimée !")
        return response


# ====================== CRUD PRODUITS ======================

class ProductListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Product
    template_name = 'accounts/products/product_list.html'
    context_object_name = 'products'
    paginate_by = 15

    def get_queryset(self):
        qs = Product.objects.select_related('category').order_by('-created_at')
        form = ProductSearchForm(self.request.GET)
        if form.is_valid():
            search = form.cleaned_data.get('search')
            category = form.cleaned_data.get('category')
            status = form.cleaned_data.get('status')
            if search:
                qs = qs.filter(name__icontains=search)
            if category:
                qs = qs.filter(category=category)
            if status:
                qs = qs.filter(status=status)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        form = ProductSearchForm(self.request.GET)
        qs = self.get_queryset()

        # Valeurs par défaut depuis GET
        search_val = self.request.GET.get('search', '')
        category_val = self.request.GET.get('category', '')
        status_val = self.request.GET.get('status', '')

        if form.is_valid():
            search_val = form.cleaned_data.get('search', '')
            category_val = form.cleaned_data.get('category', '')
            status_val = form.cleaned_data.get('status', '')

        ctx['search_form'] = form
        ctx['status_choices'] = Product.Status.choices
        ctx['search_filter'] = search_val
        ctx['category_filter'] = category_val
        ctx['status_filter'] = status_val

        ctx['total'] = qs.count()
        ctx['active'] = qs.filter(status=Product.Status.ACTIVE).count()
        ctx['out_of_stock'] = qs.filter(status=Product.Status.OUT_OF_STOCK).count()
        ctx['inactive'] = qs.filter(status=Product.Status.INACTIVE).count()
        return ctx


class ProductCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Product
    form_class = ProductCreateForm
    template_name = 'accounts/products/product_form.html'
    success_url = reverse_lazy('accounts:product_list')

    def form_valid(self, form):
        messages.success(self.request, f"Produit '{form.instance.name}' créé !")
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Product
    form_class = ProductCreateForm
    template_name = 'accounts/products/product_form.html'
    success_url = reverse_lazy('accounts:product_list')

    def form_valid(self, form):
        messages.success(self.request, f"Produit '{form.instance.name}' mis à jour !")
        return super().form_valid(form)


class ProductDetailView(LoginRequiredMixin, AdminRequiredMixin, DetailView):
    model = Product
    template_name = 'accounts/products/product_detail.html'
    context_object_name = 'product'


class ProductDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Product
    template_name = 'accounts/products/product_confirm_delete.html'
    success_url = reverse_lazy('accounts:product_list')

    def delete(self, request, *args, **kwargs):
        name = self.get_object().name
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f"Produit '{name}' supprimé !")
        return response



# ====================== CRUD PRODUITS ======================

from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .forms import SaleSearchForm, SaleForm, SaleItemFormSet
from apps.core.models import Sale

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin()
    def handle_no_permission(self):
        messages.error(self.request, "Accès refusé : administrateurs uniquement.")
        return redirect('accounts:login')

class SaleListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Sale
    template_name = 'accounts/sales/sale_list.html'
    context_object_name = 'sales'
    paginate_by = 15

    def get_queryset(self):
        qs = Sale.objects.select_related('cashier').order_by('-date')
        form = SaleSearchForm(self.request.GET)
        if form.is_valid():
            if form.cleaned_data['invoice_number']:
                qs = qs.filter(invoice_number__icontains=form.cleaned_data['invoice_number'])
            if form.cleaned_data['cashier']:
                qs = qs.filter(cashier=form.cleaned_data['cashier'])
            if form.cleaned_data['status']:
                qs = qs.filter(status=form.cleaned_data['status'])
            if form.cleaned_data['date_from']:
                qs = qs.filter(date__date__gte=form.cleaned_data['date_from'])
            if form.cleaned_data['date_to']:
                qs = qs.filter(date__date__lte=form.cleaned_data['date_to'])
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['search_form'] = SaleSearchForm(self.request.GET)
        ctx['total_revenue'] = sum(s.total_amount for s in ctx['sales'])
        return ctx

def sale_create(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        formset = SaleItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            sale = form.save()
            formset.instance = sale
            formset.save()
            sale.total_amount = sum(item.line_total for item in sale.items.all())
            sale.save()
            messages.success(request, f"Vente {sale.invoice_number} enregistrée.")
            return redirect('accounts:sale_list')
    else:
        form = SaleForm()
        formset = SaleItemFormSet()
    return render(request, 'accounts/sales/sale_form.html', {'form': form, 'formset': formset})

def sale_update(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    if request.method == 'POST':
        form = SaleForm(request.POST, instance=sale)
        formset = SaleItemFormSet(request.POST, instance=sale)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            sale.total_amount = sum(item.line_total for item in sale.items.all())
            sale.save()
            messages.success(request, f"Vente {sale.invoice_number} mise à jour.")
            return redirect('accounts:sale_detail', pk=sale.pk)
    else:
        form = SaleForm(instance=sale)
        formset = SaleItemFormSet(instance=sale)
    return render(request, 'accounts/sales/sale_form.html', {'form': form, 'formset': formset, 'object': sale})

class SaleDetailView(LoginRequiredMixin, AdminRequiredMixin, DetailView):
    model = Sale
    template_name = 'accounts/sales/sale_detail.html'
    context_object_name = 'sale'

class SaleDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Sale
    template_name = 'accounts/sales/sale_confirm_delete.html'
    success_url = reverse_lazy('accounts:sale_list')
    def delete(self, request, *args, **kwargs):
        sale = self.get_object()
        messages.success(request, f"Vente {sale.invoice_number} supprimée.")
        return super().delete(request, *args, **kwargs)
