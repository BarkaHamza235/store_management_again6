from django.urls import path
from . import views
from django.urls import path
from django.contrib.auth import views as auth_views  ##### import auth_views
from .views import (
    UserLoginView, UserLogoutView, UserRegisterView,   ##### ajout UserRegisterView
    EmployeeListView, EmployeeCreateView, EmployeeUpdateView,
    EmployeeDetailView, EmployeeDeleteView, EmployeeToggleStatusView
)

app_name = 'accounts'

urlpatterns = [
    # Connexion
    path('login/', views.UserLoginView.as_view(), name='login'),

    # Inscription
    path('register/', views.UserRegisterView.as_view(), name='register'),

    # Déconnexion (vue personnalisée, redirection assurée)
    path('logout/', views.UserLogoutView.as_view(), name='logout'),

    # Mot de passe oublié (password-reset)
    path('password-reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),


    # Gestion employés
    path('employees/', EmployeeListView.as_view(), name='employee_list'),
    path('employees/add/', EmployeeCreateView.as_view(), name='employee_add'),
    path('employees/<int:pk>/', EmployeeDetailView.as_view(), name='employee_detail'),
    path('employees/<int:pk>/edit/', EmployeeUpdateView.as_view(), name='employee_edit'),
    path('employees/<int:pk>/delete/', EmployeeDeleteView.as_view(), name='employee_delete'),
    path('employees/<int:pk>/toggle-status/', EmployeeToggleStatusView.as_view(), name='employee_toggle_status'),
]



