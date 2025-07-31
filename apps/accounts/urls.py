from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'accounts'

urlpatterns = [
    # Page de connexion
    path('login/', views.UserLoginView.as_view(), name='login'),

    # Page d'inscription
    path('register/', views.UserRegisterView.as_view(), name='register'),

    # Déconnexion - SOLUTION : Utiliser la vue personnalisée UserLogoutView
    path('logout/', views.UserLogoutView.as_view(), name='logout'),

    # Récupération mot de passe - CORRIGÉ
    path('password-reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
