from django.urls import path
from . import views

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
]
