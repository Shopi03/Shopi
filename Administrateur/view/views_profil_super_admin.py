from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def profil_super_admin(request):
    """
    Affiche le profil du super admin connecté
    """

    user = request.user

    # Vérifier que c'est bien un super admin
    if user.role != "super_admin":
        messages.error(request, "Accès non autorisé.")
        return redirect("login")

    context = {
        "super_admin": user
    }

    return render(
        request,
        "administrateur/composant/profil/profil_super_admin.html",
        context
    )



