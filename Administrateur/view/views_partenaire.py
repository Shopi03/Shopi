# views_partenaire.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

import re
from datetime import timedelta

from Localisation.models import Code_creation
from Partenaire.models import Partenaire

User = get_user_model()


@login_required
def gestion_partenaire(request):

    # ==========================================================
    # SECURITE : seul le super_admin peut accéder
    # ==========================================================
    if request.user.role != "super_admin":
        messages.error(request, "Accès refusé.")
        return redirect("login")

    # ==========================================================
    # REINITIALISATION DES CODES NON VERIFIES APRES 48 HEURES
    # ==========================================================
    limite = timezone.now() - timedelta(days=2)

    codes_expire = Code_creation.objects.filter(
        type_compte="partenaire",
        utilise=True,
        date_creation__lt=limite
    )

    for code in codes_expire:
        code.utilise = False
        code.save()

    # ==========================================================
    # LISTE DES PARTENAIRES
    # ==========================================================
    partenaires = Partenaire.objects.select_related("user").order_by("-user__date_joined")

    erreurs = {}
    valeurs = {}

    # ==========================================================
    # CODES DISPONIBLES
    # ==========================================================
    codes_disponibles = Code_creation.objects.filter(
        type_compte="partenaire",
        utilise=False
    )

    # ==========================================================
    # TRAITEMENT FORMULAIRE
    # ==========================================================
    if request.method == "POST":

        partenaire_id = request.POST.get("id")
        email = request.POST.get("email")
        telephone = request.POST.get("telephone")
        statut = request.POST.get("statut")
        code_val = request.POST.get("code_creation")

        valeurs = request.POST

        # ======================================================
        # MODIFICATION PARTENAIRE
        # ======================================================
        if partenaire_id:

            partenaire = get_object_or_404(Partenaire, id=partenaire_id)
            user = partenaire.user

            user.email = email
            user.telephone = telephone

            if hasattr(user, "statut"):
                user.statut = statut

            user.save()

            messages.success(request, "Partenaire modifié avec succès.")
            return redirect("gestion_partenaire")

        # ======================================================
        # CREATION PARTENAIRE
        # ======================================================
        code = Code_creation.objects.filter(
            code=code_val,
            type_compte="partenaire",
            utilise=False
        ).first()

        # ===== validation code =====
        if not code:
            erreurs["code_creation"] = "Code invalide ou déjà utilisé."

        # =======================
        # VALIDATION EMAIL
        # =======================
        if not email:
            erreurs["email"] = "Email obligatoire."

        elif not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
            erreurs["email"] = "Format d'email invalide."

        elif User.objects.filter(email=email).exists():
            erreurs["email"] = "Cet email est déjà utilisé."


        # =======================
        # VALIDATION TELEPHONE
        # =======================
        if not telephone:
            erreurs["telephone"] = "Téléphone obligatoire."

        elif not re.match(r"^[0-9]{8,15}$", telephone):
            erreurs["telephone"] = "Numéro invalide."

        elif User.objects.filter(telephone=telephone).exists():
            erreurs["telephone"] = "Ce numéro est déjà utilisé."

        # ===== validation statut =====
        if statut not in ["actif", "suspendu", "en_attente"]:
            erreurs["statut"] = "Statut invalide."

        # ======================================================
        # SAUVEGARDE
        # ======================================================
        if not erreurs:

            # Création User
            user = User.objects.create(
                email=email,
                telephone=telephone,
                role="partenaire",
                is_staff=False,
                code_creation=code
            )

            # Création Partenaire
            Partenaire.objects.create(
                user=user
            )

            # ===============================
            # MARQUER LE CODE COMME UTILISE
            # ===============================
            code.utilise = True
            code.save()

            # ==================================================
            # ENVOI EMAIL
            # ==================================================
            if statut == "actif":

                lien = "http://127.0.0.1:8000/localisation/verification_code_creation/"

                message = f"""
Bonjour,

Votre compte a été créé avec succès.

Type de compte : PARTENAIRE

Pour activer votre compte, utilisez le code suivant :

Code de vérification : {code.code}

Ensuite cliquez sur ce lien pour vérifier votre compte
et définir votre mot de passe :

{lien}

⚠️ Ce code est valable pendant 48 heures.

Si vous ne vérifiez pas votre compte dans ce délai,
le code sera automatiquement annulé.

Cordialement,
L'équipe de la plateforme
"""

                send_mail(
                    "Activation de votre compte Partenaire",
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False
                )

            messages.success(request, "Partenaire créé avec succès.")
            return redirect("gestion_partenaire")

    return render(request, "administrateur/pages_utilisateur/gestion_partenaire.html", {

        "partenaires": partenaires,
        "erreurs": erreurs,
        "valeurs": valeurs,
        "codes_disponibles": codes_disponibles

    })