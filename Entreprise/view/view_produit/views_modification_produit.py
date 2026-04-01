from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.validators import validate_image_file_extension
from django.core.exceptions import ValidationError
from django.utils import timezone
from Entreprise.models import Produit, Entreprise


@login_required(login_url="login")
def modifier_produit(request, id):
    """
    Modifier un produit existant.
    Seule l'entreprise propriétaire (role='entreprise') peut modifier.
    """

    user = request.user
    if not hasattr(user, "role") or user.role.lower() != "entreprise":
        messages.error(request, "Accès refusé. Cette action est réservée aux entreprises.")
        return redirect("login")

    # 🔹 Récupération de l'entreprise liée à l'utilisateur
    entreprise = get_object_or_404(Entreprise, user=user)

    # 🔹 Récupérer le produit appartenant à l'entreprise
    produit = get_object_or_404(Produit, id=id, entreprise=entreprise)

    # Pré-remplissage des données
    field_errors = {}
    old_data = {
        'titre': produit.titre,
        'description': produit.description,
        'fabricant': produit.fabricant,
        'marque': produit.marque,
        'categorie': produit.categorie,
        'stock': produit.stock,
        'prix': produit.prix,
        'remise': produit.remise,
        'commandes': produit.commandes,
        'statut': produit.statut,
        'visibilite': produit.visibilite,
        'meta_titre': produit.meta_titre,
        'meta_mots_cles': produit.meta_mots_cles,
        'meta_description': produit.meta_description,
        'date_publication': produit.date_publication.strftime("%Y-%m-%dT%H:%M") if produit.date_publication else '',
    }

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

        # 🔹 Validations de base
        if not titre:
            field_errors["titre"] = "Le titre du produit est obligatoire."
        if not prix:
            field_errors["prix"] = "Le prix du produit est obligatoire."
        if not stock:
            field_errors["stock"] = "Le stock est obligatoire."
        if not categorie:
            field_errors["categorie"] = "La catégorie doit être spécifiée."
        if not statut:
            field_errors["statut"] = "Le statut du produit doit être défini."
        if not visibilite:
            field_errors["visibilite"] = "La visibilité doit être choisie."
        if not description:
            field_errors["description"] = "La description est obligatoire."

        # Vérification doublon
        if Produit.objects.filter(
            titre__iexact=titre,
            marque__iexact=marque,
            entreprise=entreprise
        ).exclude(id=produit.id).exists():
            field_errors["titre"] = "Un produit avec ce titre et cette marque existe déjà."

        # Validation numérique
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
            remise = float(remise) if remise else 0
            if remise < 0 or remise > 100:
                field_errors["remise"] = "La remise doit être comprise entre 0 et 100%."
        except ValueError:
            field_errors["remise"] = "La remise doit être un nombre valide."

        try:
            commandes = int(commandes) if commandes else 0
            if commandes < 0:
                field_errors["commandes"] = "Le nombre de commandes ne peut pas être négatif."
        except ValueError:
            field_errors["commandes"] = "Le nombre de commandes doit être un entier valide."

        # Validation texte
        if len(titre) > 255:
            field_errors["titre"] = "Le titre est trop long (255 caractères max)."
        if len(description) > 1000:
            field_errors["description"] = "La description ne doit pas dépasser 1000 caractères."
        if len(meta_description) > 255:
            field_errors["meta_description"] = "La méta description ne doit pas dépasser 255 caractères."
        if len(meta_mots_cles) > 255:
            field_errors["meta_mots_cles"] = "Les mots-clés ne doivent pas dépasser 255 caractères."

        # Validation date
        if date_publication:
            try:
                date_publication = timezone.datetime.fromisoformat(date_publication)
            except ValueError:
                field_errors["date_publication"] = "Format de date invalide (AAAA-MM-JJThh:mm attendu)."

        # Validation image
        if image_principale:
            try:
                validate_image_file_extension(image_principale)
                if image_principale.size > 2 * 1024 * 1024:
                    field_errors["image_principale"] = "L'image est trop volumineuse (2 Mo max)."
            except ValidationError:
                field_errors["image_principale"] = "Format d'image invalide (JPG, PNG, WEBP)."

        # Si erreurs → re-render
        if field_errors:
            return render(request, "entreprise/modifier_produit.html", {
                "old_data": old_data,
                "field_errors": field_errors,
                "produit": produit
            })

        # 🔹 Mise à jour du produit
        produit.titre = titre
        produit.description = description
        produit.fabricant = fabricant
        produit.marque = marque
        produit.categorie = categorie
        produit.stock = stock
        produit.prix = prix
        produit.remise = remise
        produit.commandes = commandes
        produit.statut = statut
        produit.visibilite = visibilite
        produit.meta_titre = meta_titre
        produit.meta_mots_cles = meta_mots_cles
        produit.meta_description = meta_description
        produit.date_publication = date_publication or produit.date_publication
        if image_principale:
            produit.image_principale = image_principale
        produit.save()

        messages.success(request, f"✅ Le produit « {produit.titre} » a été modifié avec succès.")
        return redirect("liste_produit")

    # GET : affichage du formulaire
    return render(request, "entreprise/produit/modifier_produit.html", {
        "old_data": old_data,
        "field_errors": field_errors,
        "produit": produit
    })