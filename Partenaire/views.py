# fichier : partenaires/views.py

from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Partenaire
from django.utils import timezone
from django.contrib.auth.hashers import make_password  # Pour chiffrer le mot de passe


# -------------------------------------------------------------------
# ✅ CRÉATION D’UN PARTENAIRE
# -------------------------------------------------------------------
def creer_partenaire(request):

    """
    Création d'un partenaire avec conservation des valeurs saisies en cas d'erreur.
    """
    valeurs = {}  # dictionnaire pour garder les valeurs saisies
    
    if request.method == "POST":
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        pseudo = request.POST.get('pseudo')
        mail = request.POST.get('mail')
        genre = request.POST.get('genre')
        date_naissance_str = request.POST.get('date_naissance')
        mot_de_passe = request.POST.get('mot_de_passe')
        profil = request.FILES.get('profil')


        # Stocker les valeurs dans le dictionnaire (sauf mot de passe pour sécurité)
        valeurs = {
            'nom': nom,
            'prenom': prenom,
            'pseudo': pseudo,
            'mail': mail,
            'genre': genre,
            'date_naissance': date_naissance_str
        }

        # Vérifications
        if not all([nom, prenom, pseudo, mail, genre, date_naissance_str, mot_de_passe]):
            messages.error(request, "Tous les champs obligatoires doivent être remplis.")
            return render(request, 'partenaires/creer_partenaire.html', {'valeurs': valeurs})

        # Conversion date
        try:
            date_naissance = date.fromisoformat(date_naissance_str)
        except ValueError:
            messages.error(request, "La date de naissance est invalide.")
            return render(request, 'partenaires/creer_partenaire.html', {'valeurs': valeurs})

        # Vérification de l'âge
        today = date.today()
        age = today.year - date_naissance.year - ((today.month, today.day) < (date_naissance.month, date_naissance.day))
        if age < 20:
            messages.error(request, "Vous devez avoir au moins 20 ans pour vous inscrire.")
            return render(request, 'partenaires/creer_partenaire.html', {'valeurs': valeurs})

        # Vérification pseudo
        if Partenaire.objects.filter(pseudo=pseudo).exists():
            messages.error(request, "Ce pseudo est déjà utilisé.")
            return render(request, 'partenaires/creer_partenaire.html', {'valeurs': valeurs})

        # Vérification mail
        if Partenaire.objects.filter(mail=mail).exists():
            messages.error(request, "cet e-mail est déjà utilisé.")
            return render(request, 'partenaires/creer_partenaire.html', {'valeurs': valeurs})

        # Création du partenaire
        partenaire = Partenaire.objects.create(
            nom=nom,
            prenom=prenom,
            pseudo=pseudo,
            mail=mail,
            genre=genre,
            date_naissance=date_naissance,
            mot_de_passe=make_password(mot_de_passe),
            profil=profil
        )

        messages.success(request, f"Le partenaire {partenaire.prenom} a été ajouté avec succès !")
        return redirect('liste_partenaires')

    # GET
    return render(request, 'partenaires/creer_partenaire.html', {'valeurs': valeurs})

# -------------------------------------------------------------------


# -------------------------------------------------------------------
# ✏️ MODIFICATION D’UN PARTENAIRE
# -------------------------------------------------------------------
def modifier_partenaire(request, partenaire_id):
    """
    Vue permettant de modifier un partenaire existant.
    Les informations saisies sont conservées si la validation échoue.
    """

    partenaire = get_object_or_404(Partenaire, id=partenaire_id)

    # Initialisation des valeurs pré-remplies
    valeurs = {
        'nom': partenaire.nom,
        'prenom': partenaire.prenom,
        'pseudo': partenaire.pseudo,
        'mail': partenaire.mail,
        'genre': partenaire.genre,
        'date_naissance': partenaire.date_naissance,
    }

    if request.method == "POST":
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        pseudo = request.POST.get('pseudo')
        mail = request.POST.get('mail')
        genre = request.POST.get('genre')
        date_naissance_str = request.POST.get('date_naissance')
        mot_de_passe = request.POST.get('mot_de_passe')
        profil = request.FILES.get('profil')

        # Garder les valeurs pour réaffichage
        valeurs.update({
            'nom': nom,
            'prenom': prenom,
            'pseudo': pseudo,
            'mail': mail,
            'genre': genre,
            'date_naissance': date_naissance_str
        })

        # Vérifier que les champs obligatoires sont remplis
        if not all([nom, prenom, pseudo, mail, genre, date_naissance_str]):
            messages.error(request, "Tous les champs obligatoires doivent être remplis.")
            return render(request, 'partenaires/modifier_partenaire.html', {'valeurs': valeurs, 'partenaire': partenaire})

        # Vérifier la date de naissance
        try:
            date_naissance = date.fromisoformat(date_naissance_str)
        except ValueError:
            messages.error(request, "La date de naissance est invalide.")
            return render(request, 'partenaires/modifier_partenaire.html', {'valeurs': valeurs, 'partenaire': partenaire})

        # Vérifier l'âge
        today = date.today()
        age = today.year - date_naissance.year - ((today.month, today.day) < (date_naissance.month, date_naissance.day))
        if age < 20:
            messages.error(request, "Le partenaire doit avoir au moins 20 ans.")
            return render(request, 'partenaires/modifier_partenaire.html', {'valeurs': valeurs, 'partenaire': partenaire})

        # Vérifier unicité du pseudo et de l'email (sauf pour le même partenaire)
        if Partenaire.objects.filter(pseudo=pseudo).exclude(id=partenaire.id).exists():
            messages.error(request, "Ce pseudo est déjà utilisé.")
            return render(request, 'partenaires/modifier_partenaire.html', {'valeurs': valeurs, 'partenaire': partenaire})

        if Partenaire.objects.filter(mail=mail).exclude(id=partenaire.id).exists():
            messages.error(request, "Cet e-mail est déjà utilisé.")
            return render(request, 'partenaires/modifier_partenaire.html', {'valeurs': valeurs, 'partenaire': partenaire})

        # ✅ Si tout est correct, on met à jour
        partenaire.nom = nom
        partenaire.prenom = prenom
        partenaire.pseudo = pseudo
        partenaire.mail = mail
        partenaire.genre = genre
        partenaire.date_naissance = date_naissance

        # Mettre à jour le mot de passe seulement si l’utilisateur en saisit un nouveau
        if mot_de_passe:
            partenaire.mot_de_passe = make_password(mot_de_passe)

        # Mettre à jour le profil si une nouvelle image est fournie
        if profil:
            partenaire.profil = profil

        partenaire.save()
        messages.success(request, f"Le partenaire {partenaire.prenom} a été modifié avec succès.")
        return redirect('liste_partenaires')

    # Si GET, afficher la page avec les valeurs du partenaire existant
    return render(request, 'partenaires/modifier_partenaire.html', {'valeurs': valeurs, 'partenaire': partenaire})
# -------------------------------------------------------------------


# -------------------------------------------------------------------
# ❌ SUPPRESSION D’UN PARTENAIRE
# -------------------------------------------------------------------
def supprimer_partenaire(request, partenaire_id):
    """
    Vue permettant de supprimer un partenaire existant après confirmation.
    """

    partenaire = get_object_or_404(Partenaire, id=partenaire_id)

    if request.method == "POST":
        partenaire.delete()
        messages.success(request, "Le partenaire a été supprimé avec succès.")
        return redirect('liste_partenaires')

    return render(request, 'partenaires/supprimer_partenaire.html', {'partenaire': partenaire})
# -------------------------------------------------------------------


# -------------------------------------------------------------------
# 📋 AFFICHAGE DE TOUS LES PARTENAIRES
# -------------------------------------------------------------------
def liste_partenaires(request):
    """
    Vue affichant la liste de tous les partenaires enregistrés dans la base.
    """
    partenaires = Partenaire.objects.all().order_by('-date_creation')
    return render(request, 'partenaires/liste_partenaires.html', {'partenaires': partenaires})
# -------------------------------------------------------------------
