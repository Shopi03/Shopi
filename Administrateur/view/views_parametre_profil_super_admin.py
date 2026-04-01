from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash

@login_required
def parametre_profil_super_admin(request):
    """
    Gestion des paramètres du profil du Super Admin connecté
    """
    user = request.user

    # Vérification du rôle
    if user.role != "super_admin":
        messages.error(request, "Accès non autorisé.")
        return redirect("login")

    if request.method == "POST":
        form_type = request.POST.get("form_type")

        # ===============================
        # 🔵 Mise à jour du profil
        # ===============================
        if form_type == "update_profile":
            # Récupération des données du formulaire
            nom = request.POST.get("firstnameInput")
            prenom = request.POST.get("designationInput")
            adresse = request.POST.get("websiteInput1")
            ville = request.POST.get("cityInput")
            pays = request.POST.get("countryInput")
            date_naissance = request.POST.get("date_naissance")
            sexe = request.POST.get("sexe")

            # Mise à jour des champs si renseignés
            if nom:
                user.nom = nom
            if prenom:
                user.prenom = prenom
            if adresse:
                user.adresse = adresse
            if ville:
                user.ville = ville
            if pays:
                user.pays = pays
            if date_naissance:
                user.date_naissance = date_naissance
            if sexe:
                user.sexe = sexe

            # Gestion du profil photo
            if "logoInput" in request.FILES:
                profil_file = request.FILES["logoInput"]
                if profil_file.content_type in ["image/jpeg", "image/png"] and profil_file.size <= 2 * 1024 * 1024:
                    user.profil = profil_file
                else:
                    messages.warning(request, "Image invalide ou trop lourde (max 2MB).")

            user.save()
            messages.success(request, "Profil mis à jour avec succès.")
            return redirect("parametre_profil_super_admin")

        # ===============================
        # 🟢 Changement mot de passe
        # ===============================
        elif form_type == "change_password":
            old_password = request.POST.get("oldpasswordInput")
            new_password = request.POST.get("newpasswordInput")
            confirm_password = request.POST.get("confirmpasswordInput")

            # Vérification de l'ancien mot de passe
            if not check_password(old_password, user.password):
                messages.error(request, "Ancien mot de passe incorrect.")
                return redirect("parametre_profil_super_admin")

            # Vérification de la correspondance des mots de passe
            if new_password != confirm_password:
                messages.error(request, "Les mots de passe ne correspondent pas.")
                return redirect("parametre_profil_super_admin")

            # Vérification de la longueur
            if len(new_password) < 8:
                messages.error(request, "Le mot de passe doit contenir au moins 8 caractères.")
                return redirect("parametre_profil_super_admin")

            # Mise à jour du mot de passe
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)  # Éviter la déconnexion

            messages.success(request, "Mot de passe modifié avec succès.")
            return redirect("parametre_profil_super_admin")

    # Contexte pour le template
    context = {
        "super_admin": user
    }

    return render(
        request,
        "administrateur/composant/profil/parametre_profil_super_admin.html",
        context
    )