
# views.py (ou login_views.py si tu as séparé)

import random
from datetime import timedelta

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings

from Administrateur.models import User  # ton User personnalisé


# ou ton modèle User personnalisé
User = get_user_model()



# ==========================================================
# 🔐 LOGIN MULTI-RÔLES
# ==========================================================






def login_multi(request):
    """
    Login multi-utilisateur (email, téléphone ou nom).
    Message global en cas d'erreur.
    Redirection selon rôle.
    """
    if request.method == "POST":
        login_input = request.POST.get("login", "").strip()
        password = request.POST.get("mot_de_passe", "").strip()

        if not login_input or not password:
            messages.error(request, "Identifiant ou mot de passe incorrect.")
            return render(request, "administrateur/pages_multi/login.html", {"login": login_input})

        # Recherche rapide de l'utilisateur
        user = User.objects.filter(
            Q(email__iexact=login_input) |
            Q(telephone__iexact=login_input) |
            Q(nom__iexact=login_input)
        ).first()

        if not user:
            messages.error(request, "Identifiant ou mot de passe incorrect.")
            return render(request, "administrateur/pages_multi/login.html", {"login": login_input})

        # Authentification via email (vérifier que backend accepte email)
        authenticated_user = authenticate(
            request, 
            username=user.email,  # ou user.get_username() si AbstractBaseUser
            password=password
        )

        if not authenticated_user:
            messages.error(request, "Identifiant ou mot de passe incorrect.")
            return render(request, "administrateur/pages_multi/login.html", {"login": login_input})

        # Connexion réussie
        login(request, authenticated_user)

        # Stockage dans session
        request.session['user_id'] = authenticated_user.id
        request.session['role'] = authenticated_user.role.lower()

        # Redirection selon rôle
        redirect_map = {
            "super_admin": "tableau_de_bord_admin",
            "administrateur": "admin_dashboard",
            "entreprise": "tableau_de_bord_entreprise",
            "client": "tableau_de_bord_client",
            "livreur": "tableau_de_bord_livreur",
            "partenaire": "tableau_de_bord_partenaire",
            "correspondant": "tableau_de_bord_correspondant",
        }

        role = authenticated_user.role.lower()
        dashboard_url = redirect_map.get(role)

        if dashboard_url:
            return redirect(dashboard_url)
        else:
            messages.error(request, "Rôle non reconnu, contactez l'administrateur.")
            return redirect("login")

    return render(request, "administrateur/pages_multi/login.html")


# ==========================================================
# 🔄 RESET MOT DE PASSE SÉCURISÉ
# ==========================================================
def mot_de_passe_oubliez(request):

    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        if not email:
            messages.error(request, "Entrez votre email.")
            return redirect("mot_de_passe_oubliez")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Aucun compte trouvé.")
            return redirect("mot_de_passe_oubliez")

        code = random.randint(100000, 999999)
        request.session["reset_email"] = email
        request.session["reset_code"] = code
        request.session["reset_time"] = timezone.now().isoformat()

        send_mail(
            "Réinitialisation mot de passe",
            f"Votre code est : {code}",
            settings.DEFAULT_FROM_EMAIL,
            [email],
        )

        return redirect("verification_code")

    return render(request, "administrateur/pages_multi/mot_de_passe_oubliez.html")


def verification_code(request):
    code_session = request.session.get("reset_code")
    time_str = request.session.get("reset_time")

    if not code_session or not time_str:
        return redirect("mot_de_passe_oubliez")

    if timezone.now() - timezone.datetime.fromisoformat(time_str) > timedelta(minutes=5):
        request.session.flush()
        messages.error(request, "Code expiré.")
        return redirect("mot_de_passe_oubliez")

    if request.method == "POST":
        if request.POST.get("code") == str(code_session):
            return redirect("nouveau_mot_de_passe")
        else:
            messages.error(request, "Code incorrect.")

    return render(request, "administrateur/pages_multi/verification_code.html")


def nouveau_mot_de_passe(request):
    email = request.session.get("reset_email")
    if not email:
        return redirect("mot_de_passe_oubliez")

    if request.method == "POST":
        new_password = request.POST.get("new_password")
        confirm = request.POST.get("confirm_password")

        if new_password != confirm:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return redirect("nouveau_mot_de_passe")

        user = User.objects.get(email=email)
        user.password = make_password(new_password)
        user.save()
        request.session.flush()
        messages.success(request, "Mot de passe réinitialisé avec succès.")
        return redirect("mot_de_passe_reinitialiser")

    return render(request, "administrateur/pages_multi/nouveau_mot_de_passe.html")


def mot_de_passe_reinitialiser(request):
    return render(request, "administrateur/pages_multi/mot_de_passe_reinitialiser.html")



