from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from Partenaire.models import Partenaire

@login_required
def profil_partenaire(request):
    """
    Affiche le profil du Partenaire connecté
    """

    user = request.user

    # Vérifier que c'est bien un Partenaire
    if user.role != "partenaire":
        messages.error(request, "Accès non autorisé.")
        return redirect("login")  # ou page d'accueil sécurisée

    # Récupérer le profil Partenaire
    partenaire = get_object_or_404(Partenaire, user=user)

    context = {
        "user": user,
        "partenaire": partenaire
    }

    return render(
        request,
        "partenaire/composant/profil/profil_partenaire.html",
        context
    )


