# fichier : shopi_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Afficher tous les partenaires
    path('', views.dashboard_partenaire, name='dashboard_partenaire'),

    # Créer un nouveau partenaire
    path('creer_partenaire/', views.creer_partenaire, name='creer_partenaire'),

    # Modifier un partenaire existant (on passe l'ID du partenaire)
    path('modifier/<int:partenaire_id>/', views.modifier_partenaire, name='modifier_partenaire'),

    # Supprimer un partenaire (on passe l'ID du partenaire)
    path('supprimer/<int:partenaire_id>/', views.supprimer_partenaire, name='supprimer_partenaire'),

    # Se connecter au tableau de bord du partenaire
    path('connexion/', views.login_partenaire, name='login_partenaire'),

    # Permettre au partenaire de se déconnecter
    path('deconnexion/', views.logout_partenaire, name='logout_partenaire'),

    # Processus d'inscription en plusieurs étapes
    # path('inscription/1/', views.inscription1, name='inscription1'),
    path('ajax/verifier-email/', views.verifier_email, name='verifier_email'),
    path('ajax/verifier-pseudo/', views.verifier_pseudo, name='verifier_pseudo'),
]