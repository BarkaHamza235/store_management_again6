from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin

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
        return context

@method_decorator(login_required, name='dispatch')
class HomeRedirectView(View):
    """Redirige intelligemment selon le rôle de l'utilisateur"""

    def get(self, request):
        user = request.user

        if user.is_authenticated:
            if hasattr(user, 'role'):
                if user.role == 'ADMIN':
                    return redirect('core:dashboard')
                elif user.role == 'CASHIER':
                    return redirect('core:caisse')

            # Par défaut, redirection vers dashboard
            return redirect('core:dashboard')

        return redirect('accounts:login')


from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from .models import Supplier

class SupplierListView(LoginRequiredMixin, ListView):
    """Vue liste des fournisseurs avec recherche et filtres"""
    model = Supplier
    template_name = 'accounts/suppliers/supplier_list.html'
    context_object_name = 'suppliers'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Supplier.objects.all()
        
        # Recherche
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(contact_person__icontains=search) |
                Q(email__icontains=search) |
                Q(city__icontains=search)
            )
        
        # Filtre par statut
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Gestion des Fournisseurs'
        context['search_query'] = self.request.GET.get('search', '')
        context['status_filter'] = self.request.GET.get('status', '')
        context['status_choices'] = Supplier.Status.choices
        
        # Statistiques
        context['total_suppliers'] = Supplier.objects.count()
        context['active_suppliers'] = Supplier.objects.filter(status=Supplier.Status.ACTIVE).count()
        context['inactive_suppliers'] = Supplier.objects.filter(status=Supplier.Status.INACTIVE).count()
        context['suspended_suppliers'] = Supplier.objects.filter(status=Supplier.Status.SUSPENDED).count()
        
        return context

class SupplierCreateView(LoginRequiredMixin, CreateView):
    """Vue création d'un fournisseur"""
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
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Ajouter un Fournisseur'
        context['form_title'] = 'Nouveau Fournisseur'
        context['submit_text'] = 'Créer le Fournisseur'
        return context

class SupplierUpdateView(LoginRequiredMixin, UpdateView):
    """Vue modification d'un fournisseur"""
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
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Modifier {self.object.name}'
        context['form_title'] = f'Modifier {self.object.name}'
        context['submit_text'] = 'Sauvegarder les Modifications'
        return context

class SupplierDetailView(LoginRequiredMixin, DetailView):
    """Vue détail d'un fournisseur"""
    model = Supplier
    template_name = 'core/suppliers/supplier_detail.html'
    context_object_name = 'supplier'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Détails - {self.object.name}'
        return context

class SupplierDeleteView(LoginRequiredMixin, DeleteView):
    """Vue suppression d'un fournisseur"""
    model = Supplier
    template_name = 'core/suppliers/supplier_confirm_delete.html'
    success_url = reverse_lazy('core:supplier_list')
    
    def delete(self, request, *args, **kwargs):
        supplier_name = self.get_object().name
        result = super().delete(request, *args, **kwargs)
        messages.success(request, f"Fournisseur '{supplier_name}' supprimé avec succès.")
        return result
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Supprimer {self.object.name}'
        return context
