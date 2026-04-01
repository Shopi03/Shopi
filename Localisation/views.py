from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from django.utils import timezone

from Localisation.models import Code_creation

from Partenaire.models import Partenaire

User = get_user_model()

# Administrateur/views/views_code_creation.py


from Partenaire.models import Partenaire



# ==========================================================
# GENERATION ET LISTE DES CODES DE CREATION
# ==========================================================
import random
import string

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from Localisation.models import Code_creation
from Partenaire.models import Partenaire


def generate_random_code(prefix="", length=6):
    chars = string.ascii_uppercase + string.digits
    code = ''.join(random.choice(chars) for _ in range(length))
    return f"{prefix}{code}"


@login_required
def gestion_code_creation(request):

    if request.user.role not in ["super_admin", "administrateur", "partenaire"]:
        messages.error(request, "Accès refusé.")
        return redirect("login")

    partenaires = Partenaire.objects.all()

    codes = Code_creation.objects.select_related(
        "createur",
        "partenaire"
    ).order_by("-date_creation")

    valeurs = {}

    if request.method == "POST":

        type_compte = request.POST.get("type_compte")
        partenaire_id = request.POST.get("partenaire")
        prefix = request.POST.get("prefix", "")
        nombre = int(request.POST.get("nombre", 1))

        partenaire = None

        if partenaire_id:
            try:
                partenaire = Partenaire.objects.get(user_id=partenaire_id)
            except Partenaire.DoesNotExist:
                partenaire = None

        if type_compte == "administrateur" and request.user.role != "super_admin":
            messages.error(request, "Seul le super administrateur peut créer ce type de code.")
            return redirect("gestion_code_creation")

        # génération multiple
        codes_crees = []

        for i in range(nombre):

            code_value = generate_random_code(prefix)

            code = Code_creation.objects.create(
                code=code_value,
                type_compte=type_compte,
                createur=request.user,
                partenaire=partenaire,
                utilise=False
            )

            codes_crees.append(code.code)

        messages.success(request, f"{nombre} codes générés avec succès.")

        return redirect("gestion_code_creation")

    # statistiques

    stats = {
        "total_disponible": codes.filter(utilise=False).count(),
        "total_utilise": codes.filter(utilise=True).count(),
    }

    type_stats = {

        "livreur": {
            "disponible": codes.filter(type_compte="livreur", utilise=False).count(),
            "utilise": codes.filter(type_compte="livreur", utilise=True).count(),
        },

        "entreprise": {
            "disponible": codes.filter(type_compte="entreprise", utilise=False).count(),
            "utilise": codes.filter(type_compte="entreprise", utilise=True).count(),
        },

        "partenaire": {
            "disponible": codes.filter(type_compte="partenaire", utilise=False).count(),
            "utilise": codes.filter(type_compte="partenaire", utilise=True).count(),
        },

        "administrateur": {
            "disponible": codes.filter(type_compte="administrateur", utilise=False).count(),
            "utilise": codes.filter(type_compte="administrateur", utilise=True).count(),
        },
    }

    return render(request, "localisation/code_creation_utilisateur.html", {

        "codes": codes,
        "partenaires": partenaires,
        "stats": stats,
        "type_stats": type_stats,
        "valeurs": valeurs

    })





def verification_code_creation(request):
    """
    Vérifie un code de création pour un type de compte.
    - Si code.utilise=True et associé à un utilisateur → redirection vers modifier mot de passe
    - Sinon → message d'erreur
    """

    erreurs = {}  # pour les erreurs spécifiques à ce formulaire
    valeurs = request.POST.copy() if request.method == "POST" else {}

    if request.method == "POST":
        code_saisi = request.POST.get("code")

        if not code_saisi:
            erreurs["code"] = "Veuillez entrer un code."
            return render(request, "localisation/verification_code_creation.html",
                          {"erreurs": erreurs, "valeurs": valeurs})

        # Récupération du code
        code_obj = Code_creation.objects.filter(code=code_saisi).first()

        if not code_obj:
            erreurs["code"] = "Code invalide."
            return render(request, "localisation/verification_code_creation.html",
                          {"erreurs": erreurs, "valeurs": valeurs})

        # Si code non utilisé → impossible de continuer
        if not code_obj.utilise:
            erreurs["code"] = "Ce code n'a pas encore été activé ou a expiré."
            return render(request, "localisation/verification_code_creation.html",
                          {"erreurs": erreurs, "valeurs": valeurs})

        # Vérification expiration
        if code_obj.expiration_code and timezone.now() > code_obj.expiration_code:
            code_obj.utilise = False
            code_obj.save()
            erreurs["code"] = "Ce code a expiré."
            return render(request, "localisation/verification_code_creation.html",
                          {"erreurs": erreurs, "valeurs": valeurs})

        # Vérifier que le code est associé à un utilisateur
        utilisateur = User.objects.filter(code_creation=code_obj).first()
        if not utilisateur:
            erreurs["code"] = "Aucun utilisateur n'est associé à ce code."
            return render(request, "localisation/verification_code_creation.html",
                          {"erreurs": erreurs, "valeurs": valeurs})

        # Tout est ok → stocker utilisateur en session et rediriger
        request.session["id_utilisateur_verification"] = utilisateur.id
        messages.success(request, "Code vérifié avec succès.", extra_tags="verification")
        return redirect("modifier_mot_de_passe")

    return render(request, "localisation/verification_code_creation.html",
                  {"erreurs": erreurs, "valeurs": valeurs})

# --------------------------
# localisation/views.py




def modifier_mot_de_passe(request):
    """
    Permet à l'utilisateur vérifié de modifier son mot de passe.
    Les messages sont marqués avec 'mot_de_passe' pour filtrer dans le template.
    """

    # Récupération de l'utilisateur depuis la session
    user_id = request.session.get("id_utilisateur_verification")
    if not user_id:
        messages.error(request, "Session expirée. Veuillez vérifier votre code à nouveau.", extra_tags="mot_de_passe")
        return redirect("verification_code_creation")

    try:
        utilisateur = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, "Utilisateur introuvable.", extra_tags="mot_de_passe")
        return redirect("verification_code_creation")

    erreurs = {}

    if request.method == "POST":
        password = request.POST.get("password")
        password_confirm = request.POST.get("password_confirm")

        # Validation simple
        if not password or not password_confirm:
            erreurs["password"] = "Veuillez remplir tous les champs."
        elif password != password_confirm:
            erreurs["password"] = "Les mots de passe ne correspondent."

        if not erreurs:
            # Mise à jour sécurisée du mot de passe
            utilisateur.password = make_password(password)
            utilisateur.save()

            # Suppression de l'utilisateur de la session après modification
            del request.session["id_utilisateur_verification"]

            messages.success(request, "Mot de passe modifié avec succès.", extra_tags="mot_de_passe")
            return redirect("login")  # Rediriger vers login après succès

    return render(request, "localisation/mot_de_passe_modifier.html", {
        "erreurs": erreurs
    })