from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from Entreprise.models import Livreur, Entreprise
from django.contrib.auth import get_user_model
import random, string, traceback

User = get_user_model()  # Récupère ton modèle User personnalisé

@login_required(login_url="login")
def liste_livreurs(request):
    """
    Liste des livreurs + ajout / modification.
    Lie automatiquement les livreurs à l'entreprise connectée via role.
    """

    # Vérifie que l'utilisateur connecté est bien une entreprise
    if request.user.role != "entreprise":
        return redirect("login")

    # Récupère l'entreprise liée à l'utilisateur
    entreprise_obj = get_object_or_404(Entreprise, user=request.user)

    # Liste des livreurs liés à cette entreprise
    livreurs = Livreur.objects.filter(entreprise=entreprise_obj).order_by("-date_creation")

    erreurs = {}
    valeurs = {}

    if request.method == "POST":
        data = request.POST
        livreur_id = data.get("id", "").strip()

        prenom = data.get("prenom", "").strip()
        nom = data.get("nom", "").strip()
        email = data.get("email", "").strip()
        telephone = data.get("telephone", "").strip()
        vehicule = data.get("vehicule", "").strip()
        zone = data.get("zone", "").strip()
        statut = data.get("statut", "").strip()
        mot_de_passe = data.get("mot_de_passe", "").strip()

        valeurs = data

        # =========================
        # VALIDATION
        # =========================
        if not prenom:
            erreurs["prenom"] = "Le prénom est obligatoire."
        if not nom:
            erreurs["nom"] = "Le nom est obligatoire."
        if not email:
            erreurs["email"] = "L'email est obligatoire."
        else:
            exclude_id = int(livreur_id) if livreur_id.isdigit() else None
            if Livreur.objects.filter(user__email=email, entreprise=entreprise_obj).exclude(id=exclude_id).exists():
                erreurs["email"] = "Cet email est déjà utilisé."
        if not telephone:
            erreurs["telephone"] = "Le téléphone est obligatoire."
        else:
            exclude_id = int(livreur_id) if livreur_id.isdigit() else None
            if Livreur.objects.filter(user__telephone=telephone, entreprise=entreprise_obj).exclude(id=exclude_id).exists():
                erreurs["telephone"] = "Ce téléphone est déjà utilisé."
        if statut not in ["actif", "suspendu", "en_attente"]:
            erreurs["statut"] = "Statut invalide."

        # =========================
        # CREATION OU MODIFICATION
        # =========================
        if livreur_id and livreur_id.isdigit():
            # Modification existante
            livreur = get_object_or_404(Livreur, id=int(livreur_id), entreprise=entreprise_obj)
            nouveau_compte = False
            user = livreur.user
        else:
            # Création d'un nouvel utilisateur + livreur
            if not mot_de_passe:
                mot_de_passe = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

            user = User.objects.create(
                email=email,
                prenom=prenom,  # adapte selon ton modèle User
                nom=nom,
                telephone=telephone
            )
            user.set_password(mot_de_passe)
            user.save()

            livreur = Livreur(entreprise=entreprise_obj, user=user)
            nouveau_compte = True

        # =========================
        # SAUVEGARDE
        # =========================
        if not erreurs:
            # Mise à jour user
            user.prenom = prenom
            user.nom = nom
            user.email = email
            user.telephone = telephone
            if mot_de_passe:
                user.set_password(mot_de_passe)
            user.save()

            # Mise à jour livreur
            livreur.vehicule = vehicule
            livreur.zone_livraison = zone
            livreur.statut = statut
            livreur.save()

            # =========================
            # ENVOI EMAIL SI NOUVEAU COMPTE ACTIF
            # =========================
            if statut == "actif" and nouveau_compte:
                try:
                    # Génération du token et code
                    livreur.generer_token()  # Assurez-vous que cette méthode existe

                    verification_url = request.build_absolute_uri(
                        reverse("verification_code_livreur", args=[livreur.confirmation_token])
                    )

                    subject = "Confirmez votre compte livreur"
                    text_content = (
                        f"Bonjour {prenom},\n\n"
                        f"Votre compte livreur a été créé.\n"
                        f"Pour le confirmer, cliquez sur le lien suivant : {verification_url}\n\n"
                        f"Ou utilisez ce code : {livreur.code_verification}\n\n"
                        f"Ce lien et ce code expirent dans 1 heure.\n"
                        f"Mot de passe temporaire : {mot_de_passe}"
                    )

                    html_content = f"""
                    <h3>Confirmation de votre compte</h3>
                    <p>Bonjour {prenom},</p>
                    <p>Votre compte livreur a été créé par l'entreprise.</p>
                    <p>Cliquez sur le bouton ci-dessous pour confirmer :</p>
                    <a href="{verification_url}"
                       style="background:#0ab39c;color:white;padding:12px 20px;text-decoration:none;border-radius:5px;">
                       Confirmer mon compte
                    </a>
                    <p style="margin-top:15px;">
                        Code de confirmation : <strong>{livreur.code_verification}</strong>
                    </p>
                    <p>Mot de passe temporaire : <strong>{mot_de_passe}</strong></p>
                    <p>Ce lien et ce code expirent dans 1 heure.</p>
                    """

                    email_message = EmailMultiAlternatives(
                        subject, text_content, settings.DEFAULT_FROM_EMAIL, [user.email]
                    )
                    email_message.attach_alternative(html_content, "text/html")
                    email_message.send(fail_silently=False)

                except Exception as e:
                    print(f"Erreur envoi email confirmation: {e}")
                    traceback.print_exc()

            return redirect("liste_livreur")

    context = {
        "livreurs": livreurs,
        "erreurs": erreurs,
        "valeurs": valeurs
    }

    return render(request, "entreprise/livreur/livreurs.html", context)