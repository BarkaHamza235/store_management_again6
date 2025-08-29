# apps/core/urls.py

from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'core'

urlpatterns = [
    # Dashboard admin
    path('dashboard/', login_required(views.DashboardView.as_view()), name='dashboard'),

    # Interface caisse
    path('caisse/', login_required(views.CaisseView.as_view()), name='caisse'),
    path('caisse/checkout/', login_required(views.caisse_checkout), name='caisse_checkout'),
    path('caisse/sale-info/', login_required(views.sale_info), name='sale_info'),
    path('caisse/generate-invoice/', login_required(views.generate_invoice), name='generate_invoice'),

    # Page d'accueil (redirection intelligente)
    path('home/', views.HomeRedirectView.as_view(), name='home'),

    # Rapports
    path('reports/', login_required(views.ReportsView.as_view()), name='reports'),
]
