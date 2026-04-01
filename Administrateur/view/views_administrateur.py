import re
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model

from Localisation.models import Code_creation
from django.http import JsonResponse


User = get_user_model()


@login_required
def gestion_administrateur(request):

    if request.user.role != "super_admin":
        messages.error(request, "Accès refusé.")
        return redirect("login")

    admins = User.objects.filter(
        Q(role="administrateur") | Q(role="super_admin")
    ).select_related("code_creation").order_by("-date_joined")

    erreurs = {}
    valeurs = {}

    codes_disponibles = Code_creation.objects.filter(
        type_compte="administrateur",
        utilise=False
    )

    if request.method == "POST":

        admin_id = request.POST.get("id")
        email = request.POST.get("email", "").strip()
        telephone = request.POST.get("telephone", "").strip()
        statut = request.POST.get("statut")
        code_val = request.POST.get("code_creation", "").strip()

        valeurs = request.POST

        # =============================
        # MODIFICATION
        # =============================
        if admin_id:

            admin = get_object_or_404(User, id=admin_id)

            admin.statut = statut
            admin.save()

            messages.success(request, "Administrateur modifié avec succès.")
            return redirect("gestion_administrateur")

        # =============================
        # VALIDATION EMAIL
        # =============================
        if not email:
            erreurs["email"] = "Email obligatoire"

        elif User.objects.filter(email=email).exists():
            erreurs["email"] = "Cet email existe déjà"

        # =============================
        # VALIDATION TELEPHONE
        # =============================
        if not telephone:
            erreurs["telephone"] = "Téléphone obligatoire"

        else:

            # seulement chiffres
            if not re.match(r'^[0-9]+$', telephone):
                erreurs["telephone"] = "Le téléphone doit contenir uniquement des chiffres"

            # longueur téléphone
            elif len(telephone) < 8 or len(telephone) > 15:
                erreurs["telephone"] = "Numéro de téléphone invalide"

            # téléphone unique
            elif User.objects.filter(telephone=telephone).exists():
                erreurs["telephone"] = "Ce numéro de téléphone existe déjà"

        # =============================
        # VALIDATION CODE
        # =============================
        code = None

        if not code_val:
            erreurs["code_creation"] = "Veuillez sélectionner un code"

        else:

            code = Code_creation.objects.filter(
                code=code_val,
                type_compte="administrateur",
                utilise=False
            ).first()

            if not code:
                erreurs["code_creation"] = "Code invalide ou déjà utilisé"

        # =============================
        # CREATION ADMIN
        # =============================
        if not erreurs:

            try:

                with transaction.atomic():

                    admin = User.objects.create(

                        email=email,
                        telephone=telephone,
                        role="administrateur",
                        statut=statut,
                        is_staff=True,
                        code_creation=code
                    )

                    # marquer code utilisé
                    code.utilise = True
                    code.save()

                    # envoyer email si actif
                    if statut == "actif":

                        lien = "http://127.0.0.1:8000/localisation/verification_code_creation/"

                        message = f"""
Bonjour,

Votre compte administrateur a été créé.

Code : {code.code}

Cliquez ici pour vérifier votre compte :

{lien}
"""

                        send_mail(
                            "Création de votre compte Administrateur",
                            message,
                            settings.DEFAULT_FROM_EMAIL,
                            [email],
                            fail_silently=False
                        )

                    messages.success(request, "Administrateur créé avec succès.")
                    return redirect("gestion_administrateur")

            except Exception as e:
                messages.error(request, "Erreur lors de la création.")

    return render(request, "administrateur/pages_utilisateur/gestion_administrateur.html", {

        "admins": admins,
        "erreurs": erreurs,
        "valeurs": valeurs,
        "codes_disponibles": codes_disponibles

    })




@login_required
def toggle_admin_statut(request, id):

    admin = get_object_or_404(User, id=id)

    if admin.statut == "actif":
        admin.statut = "suspendu"
    else:
        admin.statut = "actif"

    admin.save()

    return JsonResponse({
        "success": True,
        "statut": admin.statut
    })