from django.shortcuts import render,redirect,get_object_or_404
from .form import EntrepriseForm, ProduitForm

from .models import Entreprise,Produit, Commande
# Create your views here.
# tableau de bord
def home(request):
    entreprise = Entreprise.objects.all()
    
    return render(request, 'Entreprise/tableau_bord.html',{'entreprises': entreprise})

# ajout entreprise
def ajout_entreprise(request):
    if request.method == 'POST':
        form = EntrepriseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = EntrepriseForm()
    return render(request, 'Entreprise/ajout_entreprise.html', {'form': form})

# modification entreprise
def modification_entreprise(request,id):
    entreprise = get_object_or_404(Entreprise, id=id)
    if request.method == 'POST':
        form = EntrepriseForm(request.POST, request.FILES, instance=entreprise)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = EntrepriseForm(instance=entreprise)
    return render(request, 'Entreprise/modification_entreprise.html', {'form': form})




#ajout du produit dans l'entreprise
def ajout_produit(request):
    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('liste_entreprise')
    else:
        form = ProduitForm()
    return render(request, 'Produit/ajout_produit.html', {'form': form})


#affichage des produits de l'entreprise
def liste_produit(request):
    produits = Produit.objects.all()
    return render(request, 'Produit/liste_produit.html', {'produits': produits})

#modification du produit dans l'entreprise
def modification_produit(request,id):
    produit = get_object_or_404(Produit, id=id)
    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES, instance=produit)
        if form.is_valid():
            form.save()
            return redirect('liste_entreprise')
    else:
        form = ProduitForm(instance=produit)
    return render(request, 'Produit/modification_produit.html', {'form': form})
