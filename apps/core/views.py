# apps/core/views.py

import json
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, View, ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q

from .models import Supplier, Sale, SaleItem, Product


class DashboardView(LoginRequiredMixin, TemplateView):
    """Vue du tableau de bord pour les administrateurs"""
    template_name = 'core/dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and hasattr(request.user, 'role'):
            if request.user.role != 'ADMIN':
                return redirect('core:caisse')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Tableau de Bord - Store Manager'
        context['user_role'] = 'Administrateur'
        return context


class CaisseView(LoginRequiredMixin, TemplateView):
    """Vue de l'interface caisse pour les caissiers"""
    template_name = 'core/caisse.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Point de Vente - Store Manager'
        context['user_role'] = 'Caissier'
        context['products'] = Product.objects.filter(status=Product.Status.ACTIVE)
        return context


@method_decorator(login_required, name='dispatch')
class HomeRedirectView(View):
    """Redirige selon le rôle de l'utilisateur"""
    def get(self, request):
        user = request.user
        if user.is_authenticated and hasattr(user, 'role'):
            if user.role == 'ADMIN':
                return redirect('core:dashboard')
            elif user.role == 'CASHIER':
                return redirect('core:caisse')
        return redirect('core:dashboard')


class SupplierListView(LoginRequiredMixin, ListView):
    model = Supplier
    template_name = 'accounts/suppliers/supplier_list.html'
    context_object_name = 'suppliers'
    paginate_by = 10

    def get_queryset(self):
        qs = Supplier.objects.all()
        search = self.request.GET.get('search')
        if search:
            qs = qs.filter(
                Q(name__icontains=search) |
                Q(contact_person__icontains=search) |
                Q(email__icontains=search) |
                Q(city__icontains=search)
            )
        status = self.request.GET.get('status')
        if status:
            qs = qs.filter(status=status)
        return qs.order_by('-created_at')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'page_title': 'Gestion des Fournisseurs',
            'search_query': self.request.GET.get('search', ''),
            'status_filter': self.request.GET.get('status', ''),
            'status_choices': Supplier.Status.choices,
            'total_suppliers': Supplier.objects.count(),
            'active_suppliers': Supplier.objects.filter(status=Supplier.Status.ACTIVE).count(),
            'inactive_suppliers': Supplier.objects.filter(status=Supplier.Status.INACTIVE).count(),
            'suspended_suppliers': Supplier.objects.filter(status=Supplier.Status.SUSPENDED).count(),
        })
        return ctx


class SupplierCreateView(LoginRequiredMixin, CreateView):
    model = Supplier
    template_name = 'core/suppliers/supplier_form.html'
    fields = [
        'name', 'contact_person', 'email', 'phone',
        'address', 'city', 'postal_code', 'country',
        'tax_number', 'payment_terms', 'credit_limit',
        'status', 'notes'
    ]
    success_url = reverse_lazy('core:supplier_list')

    def form_valid(self, form):
        messages.success(self.request, f"Fournisseur '{form.instance.name}' créé avec succès.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'page_title': 'Ajouter un Fournisseur',
            'form_title': 'Nouveau Fournisseur',
            'submit_text': 'Créer le Fournisseur'
        })
        return ctx


class SupplierUpdateView(LoginRequiredMixin, UpdateView):
    model = Supplier
    template_name = 'core/suppliers/supplier_form.html'
    fields = [
        'name', 'contact_person', 'email', 'phone',
        'address', 'city', 'postal_code', 'country',
        'tax_number', 'payment_terms', 'credit_limit',
        'status', 'notes'
    ]
    success_url = reverse_lazy('core:supplier_list')

    def form_valid(self, form):
        messages.success(self.request, f"Fournisseur '{form.instance.name}' modifié avec succès.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'page_title': f"Modifier {self.object.name}",
            'form_title': f"Modifier {self.object.name}",
            'submit_text': 'Sauvegarder les Modifications'
        })
        return ctx


class SupplierDetailView(LoginRequiredMixin, DetailView):
    model = Supplier
    template_name = 'core/suppliers/supplier_detail.html'
    context_object_name = 'supplier'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = f"Détails - {self.object.name}"
        return ctx


class SupplierDeleteView(LoginRequiredMixin, DeleteView):
    model = Supplier
    template_name = 'core/suppliers/supplier_confirm_delete.html'
    success_url = reverse_lazy('core:supplier_list')

    def delete(self, request, *args, **kwargs):
        name = self.get_object().name
        res = super().delete(request, *args, **kwargs)
        messages.success(request, f"Fournisseur '{name}' supprimé avec succès.")
        return res

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = f"Supprimer {self.object.name}"
        return ctx


@login_required
@csrf_exempt
def caisse_checkout(request):
    """Finalise la vente depuis la Caisse (AJAX)"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Méthode non autorisée'}, status=405)
    data = json.loads(request.body)
    items = data.get('items', [])
    payment_mode = data.get('payment_mode')
    cash_received = data.get('cash_received', 0)

    invoice = f"F{Sale.objects.count()+1:06d}"
    sale = Sale.objects.create(
        invoice_number=invoice,
        cashier=request.user,
        customer_name="Client",
        status=Sale.Status.PAID,
        total_amount=0
    )
    total = 0
    for it in items:
        prod = get_object_or_404(Product, pk=it['sku'])
        qty = int(it['qty'])
        up = float(it['price'])
        line = SaleItem.objects.create(
            sale=sale, product=prod, quantity=qty, unit_price=up
        )
        total += line.line_total

    sale.total_amount = total
    sale.save()
    url = reverse_lazy('accounts:sale_detail', args=[sale.pk])
    return JsonResponse({'success': True, 'redirect_url': str(url)})
