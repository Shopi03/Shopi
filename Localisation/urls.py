# Localisation/urls.py

from django.urls import path
from .views import *

urlpatterns = [

    # ==========================================================
    # 🔹 GESTION DES CODES DE CRÉATION
    # accès : super_admin / administrateur / partenaire
    # ==========================================================

    path(
        "gestion_code_creation/",
        gestion_code_creation,
        name="gestion_code_creation"
    ),
    path("verification_code_creation/",verification_code_creation, name="verification_code_creation"),
    path("modifier_mot_de_passe/",modifier_mot_de_passe, name="modifier_mot_de_passe"),

]