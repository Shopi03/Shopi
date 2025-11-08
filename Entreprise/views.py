from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils.html import escape
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password
from .models import Entreprise
import re
import os


#affichage de tableau de boad 
def tableau_bord(request):
    return render(request, 'Entreprise/tableau_de_bord.entreprise.html')



# Create your views here.
# tableau de bord
def home(request):
    entreprise = Entreprise.objects.all()
    
    return render(request, 'Entreprise/tableau_bord.html',{'entreprises': entreprise})

# ajout entreprise

# ➕ Inscription d'une entreprise


def creer_entreprise(request):
    errors = {}
    data = {}

    if request.method == "POST":
        # --- Récupération et nettoyage des champs ---
        data['nom'] = nom = escape(request.POST.get('nom', '').strip())
        data['email'] = email = escape(request.POST.get('email', '').strip())
        data['telephone'] = telephone = escape(request.POST.get('telephone', '').strip())
        data['description'] = description = escape(request.POST.get('description', '').strip())
        data['mot_de_passe'] = mot_de_passe = request.POST.get('mot_de_passe', '')
        data['mot_de_passe_confirmation'] = mot_de_passe_confirmation = request.POST.get('mot_de_passe_confirmation', '')
        logo = request.FILES.get('logo')

        # --- Validation des champs ---
        # Nom
        if not nom:
            errors['nom'] = "Le nom est obligatoire."
        elif Entreprise.objects.filter(nom__iexact=nom).exists():
            errors['nom'] = "Ce nom d'entreprise est déjà utilisé."

        # Email
        if not email:
            errors['email'] = "L'email est obligatoire."
        else:
            try:
                validate_email(email)
            except ValidationError:
                errors['email'] = "Format d'email invalide."
            else:
                if Entreprise.objects.filter(email__iexact=email).exists():
                    errors['email'] = "Cet email est déjà utilisé."

        # Téléphone
        if not telephone:
            errors['telephone'] = "Le téléphone est obligatoire."
        else:
            if not re.fullmatch(r'\+?\d{8,15}', telephone):
                errors['telephone'] = "Numéro de téléphone invalide."
            elif Entreprise.objects.filter(telephone=telephone).exists():
                errors['telephone'] = "Ce numéro de téléphone est déjà utilisé."

        # Description
        if not description:
            errors['description'] = "La description est obligatoire."
        elif len(description) > 1000:
            errors['description'] = "La description est trop longue (max 1000 caractères)."

        # Mot de passe
        if not mot_de_passe:
            errors['mot_de_passe'] = "Le mot de passe est obligatoire."
        elif len(mot_de_passe) < 8:
            errors['mot_de_passe'] = "Le mot de passe doit contenir au moins 8 caractères."
        elif not re.search(r'[A-Z]', mot_de_passe):
            errors['mot_de_passe'] = "Le mot de passe doit contenir au moins une majuscule."
        elif not re.search(r'[a-z]', mot_de_passe):
            errors['mot_de_passe'] = "Le mot de passe doit contenir au moins une minuscule."
        elif not re.search(r'[0-9]', mot_de_passe):
            errors['mot_de_passe'] = "Le mot de passe doit contenir au moins un chiffre."
        elif not re.search(r'[!@#$%^&*(),.?":{}|<>]', mot_de_passe):
            errors['mot_de_passe'] = "Le mot de passe doit contenir au moins un caractère spécial."

        if mot_de_passe != mot_de_passe_confirmation:
            errors['mot_de_passe_confirmation'] = "Les mots de passe ne correspondent pas."

        # Logo
        if logo:
            if not logo.content_type in ['image/jpeg', 'image/png', 'image/jpg']:
                errors['logo'] = "Le logo doit être une image JPG ou PNG."
            elif logo.size > 2 * 1024 * 1024:
                errors['logo'] = "Le logo ne doit pas dépasser 2 Mo."
            else:
                # Générer un nom de fichier unique pour éviter collisions
                ext = os.path.splitext(logo.name)[1]
                logo.name = f"{get_random_string(12)}{ext}"

        # --- Création de l'entreprise si tout est OK ---
        if not errors:
            entreprise = Entreprise.objects.create(
                nom=nom,
                email=email,
                telephone=telephone,
                description=description,
                mot_de_passe=make_password(mot_de_passe),
                logo=logo
            )
            messages.success(request, "Entreprise créée avec succès !")
            return redirect('success_page')  # à remplacer par ton URL de succès

    # GET ou POST avec erreurs
    return render(request, "entreprise/creer_entreprise.html", {
        "errors": errors,
        "data": data
    })  

    return render(request, "composant/entreprise/creer_entreprise.html", {"form": form})


# 📋 Liste des entreprises
def liste_entreprise(request):
    entreprises = Entreprise.objects.all()
    return render(request, 'entreprise/liste_entreprise.html', {'entreprises': entreprises})

# ✏️ Modification
# def modification_entreprise(request, id):
#     entreprise = get_object_or_404(Entreprise, id=id)
#     if request.method == 'POST':
#         form = EntrepriseForm(request.POST, request.FILES, instance=entreprise)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "✅ Entreprise modifiée avec succès.")
#             return redirect('liste_entreprise')
#         else:
#             messages.error(request, "❌ Corrigez les erreurs avant d’enregistrer.")
#     else:
#         form = EntrepriseForm(instance=entreprise)
#     return render(request, 'entreprise/modification_entreprise.html', {'form': form, 'entreprise': entreprise})


# from django.contrib.auth.decorators import login_required

# @login_required
# def suppression_entreprise(request, id):
#     entreprise = get_object_or_404(Entreprise, id=id)
#     entreprise.delete()
#     messages.success(request, "⚠️ Entreprise supprimée avec succès.")
#     return redirect('liste_entreprise')



# #ajout du produit dans l'entreprise
# def ajout_produit(request):
#     if request.method == 'POST':
#         form = ProduitForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('liste_entreprise')
#     else:
#         form = ProduitForm()
#     return render(request, 'Produit/ajout_produit.html', {'form': form})


# #affichage des produits de l'entreprise
# def liste_produit(request):
#     produits = Produit.objects.all()
#     return render(request, 'Produit/liste_produit.html', {'produits': produits})

# #modification du produit dans l'entreprise
# def modification_produit(request,id):
#     produit = get_object_or_404(Produit, id=id)
#     if request.method == 'POST':
#         form = ProduitForm(request.POST, request.FILES, instance=produit)
#         if form.is_valid():
#             form.save()
#             return redirect('liste_entreprise')
#     else:
#         form = ProduitForm(instance=produit)
#     return render(request, 'Produit/modification_produit.html', {'form': form})



#login de entreprise
# def entreprise_login(request):
#     if request.method == 'POST':
#         form = EntrepriseLoginForm(request.POST)
#         if form.is_valid():
#             entreprise = form.cleaned_data['entreprise']
#             # Stocker l'ID dans la session
#             request.session['entreprise_id'] = entreprise.id
#             messages.success(request, f"Bienvenue {entreprise.nom} 👋")
#             return redirect('entreprise_dashboard')  # page d'accueil entreprise
#     else:
#         form = EntrepriseLoginForm()

#     return render(request, 'entreprise/login.html', {'form': form})


# la deconnection de l'entreprise 


# def entreprise_logout(request):
#     if 'entreprise_id' in request.session:
#         del request.session['entreprise_id']
#     messages.info(request, "Déconnexion réussie.")
#     return redirect('entreprise_login')


# @entreprise_login_required
# def entreprise_dashboard(request):
#     entreprise = Entreprise.objects.get(id=request.session['entreprise_id'])
#     return render(request, 'entreprise/dashboard.html', {'entreprise': entreprise})