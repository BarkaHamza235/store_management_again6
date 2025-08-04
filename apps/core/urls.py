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


from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # URLs existantes...
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('caisse/', views.CaisseView.as_view(), name='caisse'),
    path('home/', views.HomeRedirectView.as_view(), name='home'),
    
    # URLs Fournisseurs
    path('suppliers/', views.SupplierListView.as_view(), name='supplier_list'),
    path('suppliers/add/', views.SupplierCreateView.as_view(), name='supplier_create'),
    path('suppliers/<int:pk>/', views.SupplierDetailView.as_view(), name='supplier_detail'),
    path('suppliers/<int:pk>/edit/', views.SupplierUpdateView.as_view(), name='supplier_update'),
    path('suppliers/<int:pk>/delete/', views.SupplierDeleteView.as_view(), name='supplier_delete'),
]
