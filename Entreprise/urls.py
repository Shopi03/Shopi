from django.contrib import admin
from django.urls import path
from Entreprise.view import views  # vues de l'app Administrateur
from Client import views as client_views
from Livreur.view import views as livreur_views
from Partenaire.view import views as partenaire_views
from correspondant import views as correspondant_views

urlpatterns = [
   

    # # ---------------- DASHBOARDS ----------------

    path("tableau_de_bord_entreprise/", views.tableau_de_bord, name="tableau_de_bord_entreprise"),
   
    # ---------------- ENTREPRISE ----------------
   
    path("profil_entreprise/", views.profil_entreprise, name="profil_entreprise"),
    path("parametre_profil_entreprise/", views.parametre_profil_entreprise, name="parametre_profil_entreprise"),

    # Gestion des produits entreprise
    path("ajout_produit/", views.ajout_produit, name="ajout_produit"),
    path("liste_produit/", views.liste_produit, name="liste_produit"),
    path("produit/modifier/<int:id>/", views.modifier_produit, name="modifier_produit"),
    path("produit/supprimer/<int:id>/", views.supprimer_produit, name="supprimer_produit"),
    # path("detaille_produit/", views.detaille_produit, name="detaille_produit"),

    # Gestion des livreurs entreprise
    path("liste_livreur/", views.liste_livreurs, name="liste_livreur"),
]