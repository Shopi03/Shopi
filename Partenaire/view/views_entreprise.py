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
from Entreprise.models import Entreprise

User = get_user_model()


@login_required
def gestion_entreprise_partenaire(request):
    """
    Gestion complète des entreprises :
    - Super admin : voit et peut modifier toutes les entreprises
    - Administrateur / Partenaire : voit uniquement celles qu'ils ont créées, peut ajouter mais pas modifier
    """

    # 🔐 Sécurité : les autres utilisateurs ne peuvent pas accéder
    if request.user.role not in ["super_admin", "administrateur", "partenaire"]:
        messages.error(request, "Accès refusé.")
        return redirect("login")  # Vérifier que le nom du login est correct

    # Réinitialiser les codes expirés (48h)
    limite = timezone.now() - timedelta(days=2)
    codes_expire = Code_creation.objects.filter(
        type_compte="entreprise",
        utilise=True,
        date_creation__lt=limite
    )
    for code in codes_expire:
        code.utilise = False
        code.save()

    # Liste des entreprises selon rôle
    if request.user.role == "super_admin":
        entreprises = Entreprise.objects.select_related("user").order_by("-user__date_joined")
    else:
        entreprises = Entreprise.objects.select_related("user").filter(
            user__code_creation__createur=request.user
        ).order_by("-user__date_joined")

    erreurs = {}
    valeurs = {}

    # Codes disponibles
    if request.user.role == "super_admin":
        codes_disponibles = Code_creation.objects.filter(type_compte="entreprise", utilise=False)
    else:
        codes_disponibles = Code_creation.objects.filter(
            type_compte="entreprise",
            utilise=False,
            createur=request.user
        )

    # =====================================================
    # Traitement POST
    # =====================================================
    if request.method == "POST":
        entreprise_id = request.POST.get("id")
        email = request.POST.get("email")
        telephone = request.POST.get("telephone")
        statut = request.POST.get("statut")
        designation = request.POST.get("designation")
        description = request.POST.get("description")
        website = request.POST.get("website")
        code_val = request.POST.get("code_creation")

        valeurs = request.POST

        # ================= Modification =================
        if entreprise_id:
            # Seul super_admin peut modifier
            if request.user.role != "super_admin":
                messages.error(request, "Vous n'avez pas le droit de modifier cette entreprise.")
                return redirect("gestion_entreprise")

            entreprise = get_object_or_404(Entreprise, id=entreprise_id)
            user = entreprise.user

            user.email = email
            user.telephone = telephone
            if statut in ["actif", "suspendu", "en_attente"]:
                user.statut = statut
            user.save()

            entreprise.designation = designation
            entreprise.description = description
            entreprise.website = website
            entreprise.save()

            messages.success(request, "Entreprise modifiée avec succès.")
            return redirect("gestion_entreprise")

        # ================= Création =================
        code = Code_creation.objects.filter(
            code=code_val,
            type_compte="entreprise",
            utilise=False
        ).first()

        if not code:
            erreurs["code_creation"] = "Code invalide ou déjà utilisé."

        # Validation email
        if not email:
            erreurs["email"] = "Email obligatoire."
        elif not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
            erreurs["email"] = "Format d'email invalide."
        elif User.objects.filter(email=email).exists():
            erreurs["email"] = "Cet email est déjà utilisé."

        # Validation téléphone
        if not telephone:
            erreurs["telephone"] = "Téléphone obligatoire."
        elif not re.match(r"^[0-9]{8,15}$", telephone):
            erreurs["telephone"] = "Numéro invalide."
        elif User.objects.filter(telephone=telephone).exists():
            erreurs["telephone"] = "Ce numéro est déjà utilisé."

        # Validation statut
        if statut not in ["actif", "suspendu", "en_attente"]:
            erreurs["statut"] = "Statut invalide."

        # ================= Sauvegarde =================
        if not erreurs:
            # Création user
            user = User.objects.create(
                email=email,
                telephone=telephone,
                role="entreprise",
                statut=statut,
                code_creation=code
            )

            # Création entreprise
            Entreprise.objects.create(
                user=user,
                designation=designation,
                description=description,
                website=website
            )

            # Marquer code utilisé
            code.utilise = True
            code.save()

            # Envoi email
            if statut == "actif":
                lien = "http://127.0.0.1:8000/localisation/verification_code_creation/"
                message = f"""
Bonjour,

Votre compte entreprise a été créé avec succès.

Code de vérification : {code.code}

Ce code est valable **48 heures seulement**.
Après ce délai, il ne pourra plus être utilisé.

Cliquez sur ce lien pour vérifier votre compte et définir votre mot de passe :

{lien}

Cordialement,
L'équipe de la plateforme
"""
                send_mail(
                    "Activation de votre compte Entreprise",
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False
                )

            messages.success(request, "Entreprise créée avec succès.")
            return redirect("gestion_entreprise_partenaire")

    return render(request, "partenaire/entreprise/gestion_entreprise_partenaire.html", {
        "entreprises": entreprises,
        "erreurs": erreurs,
        "valeurs": valeurs,
        "codes_disponibles": codes_disponibles,
        "role": request.user.role
    })