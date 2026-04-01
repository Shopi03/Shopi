

from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password  # Pour chiffrer le mot de passe
from Partenaire.decorators import partenaire_login_required
from django.http import JsonResponse


# Import des modèles
from Entreprise.models import Entreprise
from Client.models import Client
from Livreur.models import Livreur
from Partenaire.models import Partenaire
from correspondant.models import Correspondant
from Administrateur.models import User

from .views_entreprise import *
from .views_livreur import *
from .views_profil_partenaire import *
from .views_parametre_profil_partenaire import *









@login_required
def tableau_de_bord_partenaire(request):
    """
    Vue affichant le tableau de bord du partenaire connecté.
    Utilise directement request.user pour récupérer le partenaire.
    Affiche le total de livreurs et d'entreprises créés par ce partenaire.
    """

    # ------------------------------------------------------
    # Vérifier que l'utilisateur est bien un partenaire
    # ------------------------------------------------------
    if getattr(request.user, "role", "").lower() != "partenaire":
        return redirect("login")  # rediriger si pas partenaire

    partenaire = request.user

    # ------------------------------------------------------
    # Total de livreurs créés par ce partenaire
    # ------------------------------------------------------
    total_livreurs = Livreur.objects.filter(
        user__code_creation__createur=partenaire
    ).count()

    # ------------------------------------------------------
    # Total d'entreprises créées par ce partenaire
    # ------------------------------------------------------
    total_entreprises = Entreprise.objects.filter(
        user__code_creation__createur=partenaire
    ).count()

    # ------------------------------------------------------
    # Contexte pour le template
    # ------------------------------------------------------
    context = {
        "total_livreurs": total_livreurs,
        "total_entreprises": total_entreprises,
        "partenaire": partenaire,
    }

    return render(
        request,
        "partenaire/tableau_de_bord.partenaire.html",
        context
    )











