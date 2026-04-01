from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from Entreprise.models import Entreprise

@login_required(login_url="login")
def profil_entreprise(request):
    """
    Affiche le profil complet de l'entreprise connectée.
    """

    user = request.user

    # Vérifier que l'utilisateur est bien une entreprise
    if not hasattr(user, "role") or user.role.lower() != "entreprise":
        messages.error(request, "Accès non autorisé.")
        return redirect("login")

    # Récupérer le profil Entreprise lié au User
    entreprise = get_object_or_404(Entreprise, user=user)

    context = {
        "user": user,
        "entreprise": entreprise
    }

    return render(
        request,
        "entreprise/composant/profil/profil_entreprise.html",
        context
    )