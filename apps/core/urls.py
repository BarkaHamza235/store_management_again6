from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'core'

urlpatterns = [
    # Dashboard admin
    path('dashboard/', login_required(views.DashboardView.as_view()), name='dashboard'),

    # Interface caisse
    path('caisse/', login_required(views.CaisseView.as_view()), name='caisse'),

    # Page d'accueil (redirection intelligente)
    path('home/', views.HomeRedirectView.as_view(), name='home'),
]
