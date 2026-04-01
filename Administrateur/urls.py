# Administrateur/urls.py

from django.urls import path
from Administrateur.view import views  # <-- importer le module views correctement

# Si tu veux utiliser d'autres apps, tu peux décommenter et importer comme ceci :
# from Entreprise import views as entreprise_views
# from Client import views as client_views
# from Livreur import views as livreur_views
# from Partenaire import views as partenaire_views
# from correspondant import views as correspondant_views

urlpatterns = [


    # ---------------- DASHBOARDS ----------------
    path("verification_super_admin/", views.verification_super_admin_code, name="verification_super_admin"),
    path("tableau_de_bord_admin/", views.tableau_de_bord_admin, name="tableau_de_bord_admin"),
    path("create.super.admin/", views.create_super_admin, name="create_super_admin"),
    

    #----------------GESTION DE PROFIL DE SUPER ADMIN-----------------------------
    path("profil_super_admin/", views.profil_super_admin, name="profil_super_admin"),
    path("parametre_profil/", views.parametre_profil_super_admin, name="parametre_profil_super_admin"),
    # ---------------- GESTION DES UTILISATEURS ----------------------------------
    path("gestion_partenaire/", views.gestion_partenaire, name="gestion_partenaire"),
    path("gestion_administrateur/", views.gestion_administrateur, name="gestion_administrateur"),
    path("gestion_entreprise/", views.gestion_entreprise, name="gestion_entreprise"),
    path("gestion_livreur/", views.gestion_livreur, name="gestion_livreur"),
    # path("gestion_correspondant/", views.gestion_correspondant, name="gestion_correspondant"),
    # path("gestion_client/", views.gestion_client, name="gestion_client"),
]