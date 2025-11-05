from django.db import models
from Client.models import Client
from Livreur.models import Livreur


#creation de modele entreprise
class Entreprise(models.Model):
    nom = models.CharField(max_length=200)
    email = models.EmailField()
    telephone = models.CharField(max_length=15)
    logo = models.ImageField(upload_to='entreprise_logos/', null=True, blank=True)
    description = models.TextField()
    date_creation = models.DateField(auto_now_add=True)
    actif = models.BooleanField(default=True)

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = "Entreprise"
        verbose_name_plural = "Entreprises"

# creation de modele produit
class Produit(models.Model):
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE)
    nom = models.CharField(max_length=200)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='produit_images/', null=True, blank=True)
    categorie = models.CharField(max_length=100)
    sous_categorie = models.CharField(max_length=100)
    marque = models.CharField(max_length=100)
    couleur = models.CharField(max_length=50)
    taille = models.CharField(max_length=20)
    poids = models.DecimalField(max_digits=10, decimal_places=2)
    disponibilite = models.BooleanField(default=True)
    date_ajout = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} - {self.entreprise.nom}"

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
        

# creation de modele commande
class Commande(models.Model):
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    #
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()
    date_commande = models.DateField(auto_now_add=True)
    statut = models.CharField(max_length=50)

    def __str__(self):
        return f"Commande {self.id} - {self.entreprise.nom}"

    class Meta:
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"