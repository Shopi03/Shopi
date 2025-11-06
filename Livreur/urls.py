
from django.urls import path
from . import views

urlpatterns = [
    # Afficher tous les livreurs
    path('', views.liste_livreurs, name='liste_livreurs'),

    # Créer un nouveau livreur
    path('creer_livreur/', views.creer_livreur, name='creer_livreur'),

    # Modifier un livreur existant (on passe l'ID du livreur)
    path('modifier/<int:livreur_id>/', views.modifier_livreur, name='modifier_livreur'),

    # Supprimer un livreur (on passe l'ID du livreur)
    path('supprimer/<int:livreur_id>/', views.supprimer_livreur, name='supprimer_livreur'),

    # Se connecter au tableau de bord du livreur
    path('connexion/', views.login_livreur, name='login_livreur'),

    # Permettre au livreur de se déconnecter
    path('deconnexion/', views.logout_livreur, name='logout_livreur'),
]