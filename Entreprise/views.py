from django.shortcuts import render,redirect,get_object_or_404
from .form import EntrepriseForm,EntrepriseLoginForm

from .models import Entreprise,Produit, Commande
from .decorateur import entreprise_login_required

from django.contrib import messages


#affichage de tableau de boad 
def tableau_bord(request):
    return render(request, 'Entreprise/tableau_de_bord.entreprise.html')

def contenu(request):
    return render(request,"Entreprise/composant/entreprise/contenu.html")

# Create your views here.
# tableau de bord
def home(request):
    entreprise = Entreprise.objects.all()
    
    return render(request, 'Entreprise/tableau_bord.html',{'entreprises': entreprise})

# ajout entreprise

# ➕ Inscription d'une entreprise
def inscription_entreprise(request):
    if request.method == 'POST':
        form = EntrepriseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Entreprise inscrite avec succès.")
            return redirect('liste_entreprises')
        else:
            messages.error(request, "❌ Veuillez corriger les erreurs ci-dessous.")
    else:
        form = EntrepriseForm()
    return render(request, 'entreprise/inscription_entreprise.html', {'form': form})

# 📋 Liste des entreprises
def liste_entreprise(request):
    entreprises = Entreprise.objects.all()
    return render(request, 'entreprise/liste_entreprise.html', {'entreprises': entreprises})

# ✏️ Modification
def modification_entreprise(request, id):
    entreprise = get_object_or_404(Entreprise, id=id)
    if request.method == 'POST':
        form = EntrepriseForm(request.POST, request.FILES, instance=entreprise)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Entreprise modifiée avec succès.")
            return redirect('liste_entreprise')
        else:
            messages.error(request, "❌ Corrigez les erreurs avant d’enregistrer.")
    else:
        form = EntrepriseForm(instance=entreprise)
    return render(request, 'entreprise/modification_entreprise.html', {'form': form, 'entreprise': entreprise})


from django.contrib.auth.decorators import login_required

@login_required
def suppression_entreprise(request, id):
    entreprise = get_object_or_404(Entreprise, id=id)
    entreprise.delete()
    messages.success(request, "⚠️ Entreprise supprimée avec succès.")
    return redirect('liste_entreprise')



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