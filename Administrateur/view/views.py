from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta
from django.contrib.auth import get_user_model
import random

# Import des modèles
from Entreprise.models import Entreprise
from Client.models import Client
from Livreur.models import Livreur
from Partenaire.models import Partenaire
from correspondant.models import Correspondant


User = get_user_model()



# # Décorateur personnalisé pour super admin
# from Administrateur.decorators import super_admin_required  



#Import des views

from .login_views import *
from .views_administrateur import *
from .views_client import *
from .views_partenaire import *
from .views_entreprise import *
from .views_livreur import *
from .views_correspondant import *
from .views_profil_super_admin import *
from .views_parametre_profil_super_admin import *

  # ou ton modèle User personnalisé


# ==========================================================
# 🔐 CONFIGURATION SÉCURITÉ SUPER ADMIN
# ==========================================================
SUPER_ADMIN_SECRET_CODE = "A9X7K2P4M8Z1Q5L3T6Y0"  # 20 caractères exact
SUPER_ADMIN_CODE_EXPIRATION_MINUTES = 3
SUPER_ADMIN_MAX_ATTEMPTS = 3


# ==========================================================
# 🔎 VÉRIFICATION RÔLE
# ==========================================================
def is_super_admin(user):
    return user.is_authenticated and getattr(user, "role", None) == "super_admin"


def super_admin_required(view_func):
    """Décorateur pour restreindre l'accès aux super admins avec code validé."""
    return user_passes_test(
        is_super_admin,
        login_url="login"
    )(view_func)


# ==========================================================
# 🔐 PAGE VÉRIFICATION CODE SECRET
# ==========================================================
# @login_required
def verification_super_admin_code(request):

    # if not is_super_admin(request.user):
    #     messages.error(request, "Accès réservé aux Super Administrateurs.")
    #     return redirect("login")

    if "super_admin_attempts" not in request.session:
        request.session["super_admin_attempts"] = 0

    if request.method == "POST":
        code = request.POST.get("code", "").strip()
        attempts = request.session.get("super_admin_attempts", 0)

        if attempts >= SUPER_ADMIN_MAX_ATTEMPTS:
            messages.error(request, "Trop de tentatives. Accès bloqué temporairement.")
            return redirect("verification_super_admin_code")

        if len(code) != 20:
            request.session["super_admin_attempts"] += 1
            messages.error(request, "Le code doit contenir exactement 20 caractères.")
            return redirect("verification_super_admin_code")

        if code == SUPER_ADMIN_SECRET_CODE:
            request.session["super_admin_verified"] = True
            request.session["super_admin_verified_time"] = timezone.now().isoformat()
            request.session["super_admin_attempts"] = 0
            messages.success(
                request,
                f"Code valide. Accès autorisé pendant {SUPER_ADMIN_CODE_EXPIRATION_MINUTES} minutes."
            )
            return redirect("create_super_admin")
        else:
            request.session["super_admin_attempts"] += 1
            remaining = SUPER_ADMIN_MAX_ATTEMPTS - request.session["super_admin_attempts"]
            messages.error(request, f"Code incorrect. Tentatives restantes : {remaining}")

    return render(request, "administrateur/composant/verification_super_admin.html")


# ==========================================================
# 👑 CRÉATION SUPER ADMIN
# ==========================================================
# @super_admin_required
def create_super_admin(request):

    verified = request.session.get("super_admin_verified")
    verified_time = request.session.get("super_admin_verified_time")

    if not verified or not verified_time:
        messages.error(request, "Vérification requise avant accès.")
        return redirect("verification_super_admin_code")

    verification_time = timezone.datetime.fromisoformat(verified_time)
    if timezone.now() - verification_time > timedelta(minutes=SUPER_ADMIN_CODE_EXPIRATION_MINUTES):
        request.session.pop("super_admin_verified", None)
        request.session.pop("super_admin_verified_time", None)
        messages.error(request, "Autorisation expirée.")
        return redirect("verification_super_admin_code")

    errors = {}
    data = {}

    if request.method == "POST":
        data["nom"] = request.POST.get("nom", "").strip()
        data["email"] = request.POST.get("email", "").strip()
        data["telephone"] = request.POST.get("telephone", "").strip()
        password = request.POST.get("mot_de_passe", "").strip()
        confirm_password = request.POST.get("mot_de_passe_confirmation", "").strip()
        profil_file = request.FILES.get("profil")

        # =========================
        # VALIDATIONS
        # =========================
        if not data["nom"]:
            errors["nom"] = "Le nom est obligatoire."
        if not data["email"]:
            errors["email"] = "L'email est obligatoire."
        if not data["telephone"]:
            errors["telephone"] = "Le téléphone est obligatoire."
        if not password:
            errors["mot_de_passe"] = "Le mot de passe est obligatoire."
        if password and len(password) < 8:
            errors["mot_de_passe"] = "Minimum 8 caractères requis."
        if password != confirm_password:
            errors["mot_de_passe_confirmation"] = "Les mots de passe ne correspondent pas."
        if User.objects.filter(email=data["email"]).exists():
            errors["email"] = "Cet email est déjà utilisé."
        if User.objects.filter(role="super_admin").count() >= 3:
            errors["role"] = "Maximum 3 Super Admins autorisés."

        # =========================
        # CRÉATION SÉCURISÉE
        # =========================
        if not errors:
            try:
                with transaction.atomic():
                    user = User.objects.create(
                        email=data["email"],
                        nom=data["nom"],
                        telephone=data["telephone"],
                        role="super_admin",
                        is_staff=True,
                        is_active=True,
                    )
                    user.set_password(password)
                    if profil_file:
                        user.profil = profil_file
                    user.save()

                request.session.pop("super_admin_verified", None)
                request.session.pop("super_admin_verified_time", None)
                messages.success(request, "Super Admin créé avec succès.")
                return redirect("login")
            except Exception as e:
                print("ERREUR CREATE SUPER ADMIN:", e)
                messages.error(request, "Erreur lors de la création.")
        else:
            messages.error(request, "Veuillez corriger les erreurs.")

    return render(request, "administrateur/create_super_admin.html", {
        "errors": errors,
        "data": data
    })


# ==========================================================
# 📊 TABLEAU DE BORD SUPER ADMIN
# ==========================================================


@super_admin_required
def tableau_de_bord_admin(request):
    """
    Tableau de bord du super admin connecté.
    Affiche les totaux, les nouveaux utilisateurs et les infos du super admin connecté.
    """

    # ----- Récupérer le super admin connecté -----
    super_admin_connecte = request.user  # Ceci est l'utilisateur actuellement connecté
    # optionnel: tu peux accéder à super_admin_connecte.nom, email, etc.

    # ----- Totaux des utilisateurs par rôle -----
    total_users = User.objects.count()
    total_super_admins = User.objects.filter(role="super_admin").count()
    total_admins = User.objects.filter(role="administrateur").count()
    total_clients = User.objects.filter(role="client").count()
    total_entreprises = User.objects.filter(role="entreprise").count()
    total_livreurs = User.objects.filter(role="livreur").count()
    total_partenaires = User.objects.filter(role="partenaire").count()
    total_correspondants = User.objects.filter(role="correspondant").count()

    # ----- Nouveaux utilisateurs sur la dernière semaine -----
    semaine = timezone.now() - timedelta(days=7)
    nouveaux_utilisateurs = User.objects.filter(date_joined__gte=semaine).count()

    # ----- Liste des super_admin récents -----
    super_admins_recents = User.objects.filter(role="super_admin").order_by("-date_joined")

    context = {
        "super_admin": super_admin_connecte,   # infos du super admin connecté
        "total_users": total_users,
        "total_super_admins": total_super_admins,
        "total_admins": total_admins,
        "total_clients": total_clients,
        "total_entreprises": total_entreprises,
        "total_livreurs": total_livreurs,
        "total_partenaires": total_partenaires,
        "total_correspondants": total_correspondants,
        "nouveaux_utilisateurs": nouveaux_utilisateurs,
        "super_admins_recents": super_admins_recents,
    }

    return render(request, "administrateur/tableau_de_bord_admin.html", context)

# ==========================================================
# 🔐 LOGIN MULTI-RÔLES
# ==========================================================


def login_multi(request):
    errors = {}
    login_input = ""

    if request.method == "POST":
        login_input = request.POST.get("login", "").strip()
        password = request.POST.get("mot_de_passe", "").strip()

        if not login_input:
            errors["login"] = "Entrez email, téléphone ou nom."
        if not password:
            errors["mot_de_passe"] = "Entrez votre mot de passe."

        if not errors:
            # Recherche utilisateur
            user = User.objects.filter(
                Q(email__iexact=login_input) |
                Q(telephone__iexact=login_input) |
                Q(nom__iexact=login_input)
            ).first()

            if not user:
                errors["login"] = "Compte introuvable."
            else:
                # Authentification via backend Django
                authenticated_user = authenticate(
                    request,
                    username=user.email,  # ou user.get_username() si AbstractBaseUser
                    password=password
                )

                if authenticated_user is not None:
                    login(request, authenticated_user)

                    # Vérifie que user.role existe
                    role = getattr(user, "role", "").lower()

                    redirect_map = {
                        "super_admin": "tableau_de_bord_admin",
                        "administrateur": "admin_dashboard",
                        "entreprise": "tableau_de_bord_entreprise",
                        "client": "tableau_de_bord_client",
                        "livreur": "tableau_de_bord_livreur",
                        "partenaire": "tableau_de_bord_partenaire",
                        "correspondant": "tableau_de_bord_correspondant",
                    }

                    return redirect(redirect_map.get(role, "login"))  # fallback
                else:
                    errors["mot_de_passe"] = "Mot de passe incorrect."

    return render(request, "administrateur/pages_multi/login.html", {
        "errors": errors,
        "login": login_input
    })


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



