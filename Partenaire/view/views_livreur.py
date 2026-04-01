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
from Livreur.models import Livreur

User = get_user_model()


@login_required
def gestion_livreur_partenaire(request):

    # =========================================
    # Réinitialisation des codes après 48h
    # =========================================

    limite = timezone.now() - timedelta(days=2)

    codes_expire = Code_creation.objects.filter(
        type_compte="livreur",
        utilise=True,
        date_creation__lt=limite
    )

    for code in codes_expire:
        code.utilise = False
        code.save()

    # =========================================
    # Liste des livreurs
    # =========================================

    livreurs = Livreur.objects.select_related(
        "user",
        "user__code_creation",
        "user__code_creation__createur"
    )

    if request.user.role != "super_admin":

        livreurs = livreurs.filter(
            user__code_creation__createur=request.user
        )

    livreurs = livreurs.order_by("-user__date_joined")

    # =========================================
    # Codes disponibles
    # =========================================

    codes_disponibles = Code_creation.objects.filter(
        type_compte="livreur",
        utilise=False
    )

    if request.user.role != "super_admin":
        codes_disponibles = codes_disponibles.filter(
            createur=request.user
        )

    erreurs = {}
    valeurs = {}

    # =========================================
    # Traitement formulaire
    # =========================================

    if request.method == "POST":

        livreur_id = request.POST.get("id")
        email = request.POST.get("email")
        telephone = request.POST.get("telephone")
        statut = request.POST.get("statut")
        code_val = request.POST.get("code_creation")

        valeurs = request.POST

        # =====================================
        # Modification livreur
        # =====================================

        if livreur_id:

            livreur = get_object_or_404(Livreur, id=livreur_id)

            user = livreur.user

            user.email = email
            user.telephone = telephone

            if request.user.role == "super_admin":
                if statut in ["actif", "suspendu", "en_attente"]:
                    user.statut = statut

            user.save()

            messages.success(request, "Livreur modifié avec succès.")

            return redirect("gestion_livreur")

        # =====================================
        # Création livreur
        # =====================================

        code = Code_creation.objects.filter(
            code=code_val,
            type_compte="livreur",
            utilise=False
        ).first()

        if not code:
            erreurs["code_creation"] = "Code invalide ou déjà utilisé."

        # ================= EMAIL =================

        if not email:
            erreurs["email"] = "L'email est obligatoire."

        elif not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
            erreurs["email"] = "Format d'email invalide."

        elif User.objects.filter(email=email).exists():
            erreurs["email"] = "Cet email est déjà utilisé."

        # ================= TELEPHONE =================

        if not telephone:
            erreurs["telephone"] = "Le téléphone est obligatoire."

        elif not re.match(r"^[0-9]{8,15}$", telephone):
            erreurs["telephone"] = "Numéro de téléphone invalide."

        elif User.objects.filter(telephone=telephone).exists():
            erreurs["telephone"] = "Ce numéro est déjà utilisé."

        # ================= STATUT =================

        if statut not in ["actif", "suspendu", "en_attente"]:
            erreurs["statut"] = "Statut invalide."

        # =====================================
        # Sauvegarde
        # =====================================

        if not erreurs:

            user = User.objects.create(
                email=email,
                telephone=telephone,
                role="livreur",
                statut=statut,
                is_staff=False,
                code_creation=code
            )

            Livreur.objects.create(
                user=user
            )

            code.utilise = True
            code.save()

            # =====================================
            # Email d'activation
            # =====================================

            if statut == "actif":

                lien_activation = "http://127.0.0.1:8000/localisation/verification_code_creation/"

                message = f"""
Bonjour,

Votre compte Livreur a été créé avec succès sur la plateforme.

----------------------------------------------------

Type de compte : LIVREUR

Code de vérification : {code.code}

----------------------------------------------------

Pour activer votre compte et définir votre mot de passe,
cliquez sur le lien ci-dessous :

{lien_activation}

Ensuite entrez le code de vérification fourni ci-dessus.

⚠️ IMPORTANT

Ce code est valable pendant 48 heures seulement.

Si le compte n'est pas activé dans ce délai,
le code sera automatiquement annulé et devra être recréé.

----------------------------------------------------

Cordialement,
L'équipe de la plateforme
"""

                send_mail(
                    "Activation de votre compte Livreur",
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False
                )

            messages.success(request, "Livreur créé avec succès.")

            return redirect("gestion_livreur_livreur")

    return render(request, "partenaire/livreur/gestion_livreur_partenaire.html", {
        "livreurs": livreurs,
        "erreurs": erreurs,
        "valeurs": valeurs,
        "codes_disponibles": codes_disponibles,
        "role": request.user.role
    })