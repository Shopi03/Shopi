# fichier : shopi_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Afficher tous les partenaires
    path('partenaires/', views.liste_partenaires, name='liste_partenaires'),

    # Créer un nouveau partenaire
    path('partenaire/creer_partenaire/', views.creer_partenaire, name='creer_partenaire'),

    # Modifier un partenaire existant (on passe l'ID du partenaire)
    path('partenaire/modifier/<int:partenaire_id>/', views.modifier_partenaire, name='modifier_partenaire'),

    # Supprimer un partenaire (on passe l'ID du partenaire)
    path('partenaire/supprimer/<int:partenaire_id>/', views.supprimer_partenaire, name='supprimer_partenaire'),
]
