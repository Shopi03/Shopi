from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from Entreprise.models import Produit, Entreprise


@login_required(login_url="login")
def liste_produit(request):
    """
    Affiche la liste des produits de l'entreprise connectée
    avec filtres All / Published / Draft et recherche.
    """

    user = request.user

    # Vérification du rôle
    if not hasattr(user, "role") or user.role.lower() != "entreprise":
        messages.error(
            request,
            "Accès refusé. Cette action est réservée aux entreprises."
        )
        return redirect("login")

    # 🔹 Récupération de l'entreprise liée à l'utilisateur
    entreprise = get_object_or_404(Entreprise, user=user)

    # 🔹 Recherche
    query = request.GET.get("q", "").strip()

    # 🔹 Produits de l'entreprise
    produits = Produit.objects.filter(entreprise=entreprise).order_by('-id')

    # 🔹 Filtre recherche
    if query:
        produits = produits.filter(
            Q(titre__icontains=query) |
            Q(categorie__icontains=query) |  # adapter si ForeignKey
            Q(statut__icontains=query)
        )

    # 🔹 Filtres par statut
    produits_published = produits.filter(statut="Published")
    produits_draft = produits.filter(statut="Draft")

    # 🔹 Compteurs
    total_count = produits.count()
    published_count = produits_published.count()
    draft_count = produits_draft.count()

    context = {
        "produits": produits,
        "produits_published": produits_published,
        "produits_draft": produits_draft,
        "total_count": total_count,
        "published_count": published_count,
        "draft_count": draft_count,
        "query": query,
        "entreprise": entreprise,
    }

    return render(request, "entreprise/produit/liste_produit.html", context)