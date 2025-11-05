# fichier : livreurs/views.py

from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Livreur
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password  # Pour chiffrer le mot de passe
from .decorators import livreur_login_required


# -------------------------------------------------------------------
#  CRÉATION D’UN livreur
# -------------------------------------------------------------------
def creer_livreur(request):

    """
    Création d'un livreur avec conservation des valeurs saisies en cas d'erreur.
    """
    valeurs = {}  # dictionnaire pour garder les valeurs saisies
    
    if request.method == "POST":
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        mail = request.POST.get('mail')
        genre = request.POST.get('genre')
        date_naissance_str = request.POST.get('date_naissance')
        mot_de_passe = request.POST.get('mot_de_passe')
        profil = request.FILES.get('profil')

        identifiant = request.POST.get('identifiant')
        telephone = request.POST.get('telephone')
        zone_livraison = request.POST.get('zone_livraison')
        vehicule = request.POST.get('vehicule')


        # Stocker les valeurs dans le dictionnaire (sauf mot de passe pour sécurité)
        valeurs = {
            'nom': nom,
            'prenom': prenom,
            'identifiant': identifiant,
            'mail': mail,
            'genre': genre,
            'date_naissance': date_naissance_str,
            'vehicule': vehicule,
            'zone_livraison': zone_livraison,
            'telephone': telephone,
        }

        # Vérifications
        if not all([nom, prenom, identifiant, mail, genre, date_naissance_str, mot_de_passe,zone_livraison,vehicule]):
            messages.error(request, "Tous les champs obligatoires doivent être remplis.")
            return render(request, 'livreurs/creer_livreur.html', {'valeurs': valeurs})

        # Conversion date
        try:
            date_naissance = date.fromisoformat(date_naissance_str)
        except ValueError:
            messages.error(request, "La date de naissance est invalide.")
            return render(request, 'livreurs/creer_livreur.html', {'valeurs': valeurs})

        # Vérification de l'âge
        today = date.today()
        age = today.year - date_naissance.year - ((today.month, today.day) < (date_naissance.month, date_naissance.day))
        if age < 19:
            messages.error(request, "Vous devez avoir au moins 19 ans pour vous inscrire.")
            return render(request, 'livreurs/creer_livreur.html', {'valeurs': valeurs})

        # Vérification identifiant
        if Livreur.objects.filter(identifiant=identifiant).exists():
            messages.error(request, "Ce identifiant est déjà utilisé.")
            return render(request, 'livreurs/creer_livreur.html', {'valeurs': valeurs})

        # Vérification mail
        if Livreur.objects.filter(mail=mail).exists():
            messages.error(request, "cet e-mail est déjà utilisé.")
            return render(request, 'livreurs/creer_livreur.html', {'valeurs': valeurs})

        if len(identifiant) != 20:
            messages.error(request, "L'identifiant doit contenir 20 caractères.")
            return render(request, 'livreurs/creer_livreur.html', {'valeurs': valeurs})

        if len(telephone) > 15:
            messages.error(request, "Le numéro de téléphone ne peut depasser 15 chiffres.")
            return render(request, 'livreurs/creer_livreur.html', {'valeurs':valeurs})

        # Création du livreur
        livreur = Livreur.objects.create(
            nom=nom,
            prenom=prenom,
            identifiant=identifiant,
            mail=mail,
            genre=genre,
            date_naissance=date_naissance,
            mot_de_passe=make_password(mot_de_passe),
            profil=profil,
            vehicule=vehicule,
            zone_livraison=zone_livraison,
            telephone=telephone,
        )

        messages.success(request, f"Le livreur {livreur.prenom} a été ajouté avec succès !")
        return redirect('liste_livreurs')

    # GET
    return render(request, 'livreurs/creer_livreur.html', {'valeurs': valeurs})

# -------------------------------------------------------------------


# -------------------------------------------------------------------
#  MODIFICATION D’UN livreur
# -------------------------------------------------------------------
def modifier_livreur(request, livreur_id):
    """
    Vue permettant de modifier un livreur existant.
    Les informations saisies sont conservées si la validation échoue.
    """

    livreur = get_object_or_404(Livreur, id=livreur_id)

    # Initialisation des valeurs pré-remplies
    valeurs = {
        'nom': livreur.nom,
        'prenom': livreur.prenom,
        'identifiant': livreur.identifiant,
        'mail': livreur.mail,
        'genre': livreur.genre,
        'date_naissance': livreur.date_naissance,
        'vehicule': livreur.vehicule,
        'zone_livraison': livreur.zone_livraison,
        'telephone': livreur.telephone,
    }

    if request.method == "POST":
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        identifiant = request.POST.get('identifiant')
        mail = request.POST.get('mail')
        genre = request.POST.get('genre')
        date_naissance_str = request.POST.get('date_naissance')
        mot_de_passe = request.POST.get('mot_de_passe')
        profil = request.FILES.get('profil')

        identifiant = request.POST.get('identifiant')
        telephone = request.POST.get('telephone')
        zone_livraison = request.POST.get('zone_livraison')
        vehicule = request.POST.get('vehicule')

        # Garder les valeurs pour réaffichage
        valeurs.update({
            'nom': nom,
            'prenom': prenom,
            'identifiant': identifiant,
            'mail': mail,
            'genre': genre,
            'date_naissance': date_naissance_str,
            'vehicule': vehicule,
            'zone_livraison': zone_livraison,
            'telephone': telephone,
        })

        # Vérifier que les champs obligatoires sont remplis
        if not all([nom, prenom, identifiant, mail, genre, date_naissance_str, vehicule, zone_livraison, telephone]):
            messages.error(request, "Tous les champs obligatoires doivent être remplis.")
            return render(request, 'livreurs/modifier_livreur.html', {'valeurs': valeurs, 'livreur': livreur})

        # Vérifier la date de naissance
        try:
            date_naissance = date.fromisoformat(date_naissance_str)
        except ValueError:
            messages.error(request, "La date de naissance est invalide.")
            return render(request, 'livreurs/modifier_livreur.html', {'valeurs': valeurs, 'livreur': livreur})

        # Vérifier l'âge
        today = date.today()
        age = today.year - date_naissance.year - ((today.month, today.day) < (date_naissance.month, date_naissance.day))
        if age < 19:
            messages.error(request, "Le livreur doit avoir au moins 19 ans.")
            return render(request, 'livreurs/modifier_livreur.html', {'valeurs': valeurs, 'livreur': livreur})

        # Vérifier unicité du identifiant et de l'email (sauf pour le même livreur)
        if Livreur.objects.filter(identifiant=identifiant).exclude(id=livreur.id).exists():
            messages.error(request, "Ce identifiant est déjà utilisé.")
            return render(request, 'livreurs/modifier_livreur.html', {'valeurs': valeurs, 'livreur': livreur})

        if Livreur.objects.filter(mail=mail).exclude(id=livreur.id).exists():
            messages.error(request, "Cet e-mail est déjà utilisé.")
            return render(request, 'livreurs/modifier_livreur.html', {'valeurs': valeurs, 'livreur': livreur})

        #  Si tout est correct, on met à jour
        livreur.nom = nom
        livreur.prenom = prenom
        livreur.identifiant = identifiant
        livreur.mail = mail
        livreur.genre = genre
        livreur.date_naissance = date_naissance
        livreur.vehicule=vehicule
        livreur.zone_livraison=zone_livraison
        livreur.telephone=telephone

        # Mettre à jour le mot de passe seulement si l’utilisateur en saisit un nouveau
        if mot_de_passe:
            livreur.mot_de_passe = make_password(mot_de_passe)

        # Mettre à jour le profil si une nouvelle image est fournie
        if profil:
            livreur.profil = profil

        livreur.save()
        messages.success(request, f"Le livreur {livreur.prenom} a été modifié avec succès.")
        return redirect('liste_livreurs')

    # Si GET, afficher la page avec les valeurs du livreur existant
    return render(request, 'livreurs/modifier_livreur.html', {'valeurs': valeurs, 'livreur': livreur})
# -------------------------------------------------------------------


# -------------------------------------------------------------------
#  SUPPRESSION D’UN livreur
# -------------------------------------------------------------------
def supprimer_livreur(request, livreur_id):
    """
    Vue permettant de supprimer un livreur existant après confirmation.
    """

    livreur = get_object_or_404(Livreur, id=livreur_id)

    if request.method == "POST":
        livreur.delete()
        messages.success(request, "Le livreur a été supprimé avec succès.")
        return redirect('liste_livreurs')

    return render(request, 'livreurs/supprimer_livreur.html', {'livreur': livreur})
# -------------------------------------------------------------------


# -------------------------------------------------------------------
#  AFFICHAGE DE TOUS LES livreurS
# -------------------------------------------------------------------
@livreur_login_required
def liste_livreurs(request):
    """
    Vue affichant la liste de tous les livreurs enregistrés dans la base.
    """
    livreurs = Livreur.objects.all().order_by('-date_creation')
    return render(request, 'livreurs/liste_livreurs.html', {'livreurs': livreurs})
# -------------------------------------------------------------------


# -------------------------------------------------------------------
#  CONNEXION DU LIVREUR
# -------------------------------------------------------------------
def login_livreur(request):
    """
    Vue permettant à un livreur de se connecter
    via son identifiant et son mot de passe.
    """

    # Si le formulaire est soumis
    if request.method == "POST":
        mail = request.POST.get('mail')
        mot_de_passe = request.POST.get('mot_de_passe')

        # Vérifier que les champs sont remplis
        if not mail or not mot_de_passe:
            messages.error(request, "Veuillez remplir tous les champs.")
            return render(request, 'livreurs/auth/login.html', {'mail': mail})

        try:
            # Vérifier si le mail existe
            livreur = Livreur.objects.get(mail=mail)

            # Vérifier le mot de passe haché
            if check_password(mot_de_passe, livreur.mot_de_passe):
                # Enregistrer la session utilisateur
                request.session['livreur_id'] = livreur.id
                request.session['livreur_nom'] = livreur.nom
                messages.success(request, f"Bienvenue {livreur.prenom} ")
                return redirect('liste_livreurs')  # ou une page d'accueil
            else:
                messages.error(request, "E-mail ou mot de passe incorrect.")
        except Livreur.DoesNotExist:
            messages.error(request, "Aucun compte trouvé avec ce mail.")

    # Si on arrive sur la page sans envoi (GET)
    return render(request, 'livreurs/auth/login.html')


# -------------------------------------------------------------------
#  DÉCONNEXION DU livreur
# -------------------------------------------------------------------
def logout_livreur(request):
    """
    Déconnecte le livreur en supprimant sa session.
    """
    if 'livreur_id' in request.session:
        del request.session['livreur_id']
        del request.session['livreur_nom']
    messages.info(request, "Vous êtes maintenant déconnecté.")
    return redirect('login_livreur')


