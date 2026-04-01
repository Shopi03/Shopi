from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .view_profil.views_profil_entreprise import *
from .view_profil.views_parametre_profil_entreprise import *
from .view_produit.views_ajout_produit import *
from .view_produit.views_liste_produit import *
from .view_produit.views_modification_produit import *
from .view_produit.views_suppression_produit import *
from .view_livreur.views_livreur import *


@login_required(login_url="login")
def tableau_de_bord(request):

    user = request.user

    # Vérifier que l'utilisateur connecté est une entreprise
    if not user.role or user.role.lower() != "entreprise":
        messages.error(request, "Accès refusé. Cette page est réservée aux entreprises.")
        return redirect("login")

    context = {
        "entreprise": user
    }

    return render(
        request,
        "entreprise/tableau_de_bord.entreprise.html",
        context
    )