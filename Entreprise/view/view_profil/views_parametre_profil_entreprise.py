from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash

from Entreprise.models import Entreprise

@login_required
def parametre_profil_entreprise(request):
    """
    Gestion des paramètres du profil de l'entreprise connectée.
    """

    user = request.user

    # Vérification du rôle
    if user.role != "entreprise":
        messages.error(request, "Accès non autorisé.")
        return redirect("login")

    # Récupération du profil entreprise via le modèle
    entreprise = get_object_or_404(Entreprise, user=user)

    if request.method == "POST":
        form_type = request.POST.get("form_type")

        # ===============================
        # 🔵 Mise à jour du profil entreprise
        # ===============================
        if form_type == "update_profile":
            # Champs User
            nom = request.POST.get("nom")
            prenom = request.POST.get("prenom")
            adresse = request.POST.get("adresse")
            ville = request.POST.get("ville")
            pays = request.POST.get("pays")
            date_naissance = request.POST.get("date_naissance")
            sexe = request.POST.get("sexe")

            # Champs Entreprise
            designation = request.POST.get("designation")
            description = request.POST.get("description")

            # Mise à jour des champs User
            if nom: user.nom = nom
            if prenom: user.prenom = prenom
            if adresse: user.adresse = adresse
            if ville: user.ville = ville
            if pays: user.pays = pays
            if date_naissance: user.date_naissance = date_naissance
            if sexe: user.sexe = sexe

            # Gestion de la photo de profil User
            profil_file = request.FILES.get("profil")
            if profil_file:
                if profil_file.content_type in ["image/jpeg", "image/png"] and profil_file.size <= 2*1024*1024:
                    user.profil = profil_file
                else:
                    messages.warning(request, "Image de profil invalide ou trop lourde (max 2MB).")

            user.save()

            # Mise à jour des champs Entreprise
            if designation: entreprise.designation = designation
            if description: entreprise.description = description

            # Gestion du logo entreprise
            logo_file = request.FILES.get("logo")
            if logo_file:
                if logo_file.content_type in ["image/jpeg", "image/png"] and logo_file.size <= 2*1024*1024:
                    entreprise.logo = logo_file
                else:
                    messages.warning(request, "Logo invalide ou trop lourd (max 2MB).")

            entreprise.save()

            messages.success(request, "Profil entreprise mis à jour avec succès.")
            return redirect("parametre_profil_entreprise")

        # ===============================
        # 🟢 Changement mot de passe
        # ===============================
        elif form_type == "change_password":
            old_password = request.POST.get("oldpasswordInput")
            new_password = request.POST.get("newpasswordInput")
            confirm_password = request.POST.get("confirmpasswordInput")

            # Vérification ancien mot de passe
            if not check_password(old_password, user.password):
                messages.error(request, "Ancien mot de passe incorrect.")
                return redirect("parametre_profil_entreprise")

            # Vérification correspondance
            if new_password != confirm_password:
                messages.error(request, "Les mots de passe ne correspondent pas.")
                return redirect("parametre_profil_entreprise")

            # Vérification longueur
            if len(new_password) < 8:
                messages.error(request, "Le mot de passe doit contenir au moins 8 caractères.")
                return redirect("parametre_profil_entreprise")

            # Mise à jour mot de passe
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)  # éviter la déconnexion

            messages.success(request, "Mot de passe modifié avec succès.")
            return redirect("parametre_profil_entreprise")

    # Contexte pour le template
    context = {
        "user": user,
        "entreprise": entreprise
    }

    return render(
        request,
        "entreprise/composant/profil/parametre_profil_entreprise.html",
        context
    )