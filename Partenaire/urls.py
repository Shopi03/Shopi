# fichier : shopi_app/urls.py

from django.urls import path
from Partenaire.view import views 

urlpatterns = [
    # Afficher tous les partenaires
    path('tableau_de_bord_partenaire', views.tableau_de_bord_partenaire, name='tableau_de_bord_partenaire'),


    path("gestion_entreprise/", views.gestion_entreprise_partenaire, name="gestion_entreprise_partenaire"),
    path("gestion_livreur/", views.gestion_livreur_partenaire, name="gestion_livreur_partenaire"),




    path("profil_partenaire/", views.profil_partenaire, name="profil_partenaire"),
    path("parametre_profil/", views.parametre_profil_partenaire, name="parametre_profil_partenaire"),


]