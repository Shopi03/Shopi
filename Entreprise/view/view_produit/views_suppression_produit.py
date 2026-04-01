from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from Entreprise.models import Produit


@login_required(login_url="login")
def supprimer_produit(request, id):
    """
    Supprime un produit appartenant à l'entreprise connectée.
    La récupération de l'entreprise se fait via request.user.
    """

    user = request.user
    if not hasattr(user, "role") or user.role.lower() != "entreprise":
        messages.error(request, "Accès refusé. Cette action est réservée aux entreprises.")
        return redirect("login")

    entreprise = user  # l'entreprise est l'utilisateur connecté

    # Récupérer le produit appartenant à l'entreprise
    produit = get_object_or_404(Produit, id=id, entreprise=entreprise)
    produit.delete()

    messages.success(request, f"✅ Le produit « {produit.titre} » a été supprimé avec succès.")
    return redirect("liste_produit")
