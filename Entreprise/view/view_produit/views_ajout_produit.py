from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_image_file_extension
from django.utils import timezone

from Entreprise.models import Produit, Entreprise


@login_required(login_url="login")
def ajout_produit(request):
    """
    Ajout d'un produit par une entreprise connectée.
    """

    user = request.user

    # Vérification du rôle
    if not hasattr(user, "role") or user.role.lower() != "entreprise":
        messages.error(
            request,
            "Accès refusé. Cette page est réservée aux entreprises."
        )
        return redirect("login")

    # Récupération de l'entreprise liée à l'utilisateur
    entreprise = get_object_or_404(Entreprise, user=user)

    old_data = {}
    field_errors = {}
    produit = None

    if request.method == "POST":

        old_data = request.POST

        titre = request.POST.get("titre", "").strip()
        description = request.POST.get("description", "").strip()
        fabricant = request.POST.get("fabricant", "").strip()
        marque = request.POST.get("marque", "").strip()
        categorie = request.POST.get("categorie", "").strip()
        stock = request.POST.get("stock", "").strip()
        prix = request.POST.get("prix", "").strip()
        remise = request.POST.get("remise", "").strip()
        commandes = request.POST.get("commandes", "").strip()
        statut = request.POST.get("statut", "").strip()
        visibilite = request.POST.get("visibilite", "").strip()
        meta_titre = request.POST.get("meta_titre", "").strip()
        meta_mots_cles = request.POST.get("meta_mots_cles", "").strip()
        meta_description = request.POST.get("meta_description", "").strip()
        date_publication = request.POST.get("date_publication", "").strip()

        image_principale = request.FILES.get("image_principale")

        # ==========================
        # VALIDATIONS
        # ==========================

        if not titre:
            field_errors["titre"] = "Le titre du produit est obligatoire."

        if not prix:
            field_errors["prix"] = "Le prix du produit est obligatoire."

        if not stock:
            field_errors["stock"] = "Le stock est obligatoire."

        if not categorie:
            field_errors["categorie"] = "La catégorie est obligatoire."

        if not statut:
            field_errors["statut"] = "Le statut du produit est obligatoire."

        if not visibilite:
            field_errors["visibilite"] = "La visibilité est obligatoire."

        if not description:
            field_errors["description"] = "La description est obligatoire."

        if not date_publication:
            field_errors["date_publication"] = "La date de publication est obligatoire."

        # Vérification doublon
        if Produit.objects.filter(
            titre__iexact=titre,
            marque__iexact=marque,
            entreprise=entreprise
        ).exists():

            field_errors["titre"] = (
                "Un produit avec ce titre et cette marque existe déjà."
            )

        # ==========================
        # VALIDATION NUMÉRIQUE
        # ==========================

        try:
            prix = float(prix)

            if prix <= 0:
                field_errors["prix"] = "Le prix doit être supérieur à zéro."

        except ValueError:
            field_errors["prix"] = "Le prix doit être un nombre valide."

        try:
            stock = int(stock)

            if stock < 0:
                field_errors["stock"] = "Le stock ne peut pas être négatif."

        except ValueError:
            field_errors["stock"] = "Le stock doit être un entier valide."

        try:
            if remise:
                remise = float(remise)

                if remise < 0 or remise > 100:
                    field_errors["remise"] = "La remise doit être entre 0 et 100 %."

        except ValueError:
            field_errors["remise"] = "La remise doit être un nombre valide."

        try:
            if commandes:
                commandes = int(commandes)

                if commandes < 0:
                    field_errors["commandes"] = (
                        "Le nombre de commandes ne peut pas être négatif."
                    )

        except ValueError:
            field_errors["commandes"] = (
                "Le nombre de commandes doit être un entier valide."
            )

        # ==========================
        # VALIDATION TEXTE
        # ==========================

        if len(titre) > 255:
            field_errors["titre"] = "Le titre est trop long (255 caractères max)."

        if len(description) > 1000:
            field_errors["description"] = (
                "La description ne doit pas dépasser 1000 caractères."
            )

        if len(meta_description) > 255:
            field_errors["meta_description"] = (
                "La méta description ne doit pas dépasser 255 caractères."
            )

        if len(meta_mots_cles) > 255:
            field_errors["meta_mots_cles"] = (
                "Les mots-clés ne doivent pas dépasser 255 caractères."
            )

        # ==========================
        # VALIDATION DATE
        # ==========================

        if date_publication:

            try:
                date_publication = timezone.datetime.fromisoformat(date_publication)

            except ValueError:
                field_errors["date_publication"] = (
                    "Format de date invalide (AAAA-MM-JJ attendu)."
                )

        # ==========================
        # VALIDATION IMAGE
        # ==========================

        if not image_principale:

            field_errors["image_principale"] = (
                "L'image principale du produit est obligatoire."
            )

        else:

            try:
                validate_image_file_extension(image_principale)

                if image_principale.size > 2 * 1024 * 1024:

                    field_errors["image_principale"] = (
                        "L'image est trop volumineuse (2 Mo maximum)."
                    )

            except Exception:

                field_errors["image_principale"] = (
                    "Fichier non valide (JPG, PNG, WEBP uniquement)."
                )

        # ==========================
        # STOP SI ERREURS
        # ==========================

        if field_errors:

            return render(
                request,
                "entreprise/produit/ajout_produit.html",
                {
                    "old_data": old_data,
                    "field_errors": field_errors,
                    "produit": produit,
                    "entreprise": entreprise,
                },
            )

        # ==========================
        # SAUVEGARDE PRODUIT
        # ==========================

        produit = Produit.objects.create(

            entreprise=entreprise,
            titre=titre,
            description=description,
            image_principale=image_principale,
            fabricant=fabricant,
            marque=marque,
            categorie=categorie,
            stock=stock,
            prix=prix,
            remise=remise or 0,
            commandes=commandes or 0,
            statut=statut,
            visibilite=visibilite,
            meta_titre=meta_titre,
            meta_mots_cles=meta_mots_cles,
            meta_description=meta_description,
            date_publication=date_publication or None,
        )

        messages.success(
            request,
            f"✅ Le produit « {produit.titre} » a été ajouté avec succès."
        )

        return redirect("ajout_produit")

    # ==========================
    # AFFICHAGE PAGE
    # ==========================

    return render(
        request,
        "entreprise/produit/ajout_produit.html",
        {
            "old_data": old_data,
            "field_errors": field_errors,
            "produit": produit,
            "entreprise": entreprise,
        },
    )