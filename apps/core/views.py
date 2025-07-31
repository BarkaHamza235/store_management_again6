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
