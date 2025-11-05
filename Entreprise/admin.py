from django.contrib import admin

from .models import Entreprise, Produit, Commande



@admin.register(Entreprise)
class EntrepriseAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'telephone', 'date_creation', 'actif')
    list_filter = ('actif',)
    search_fields = ('nom', 'email', 'telephone')
    ordering = ('nom',)
    date_hierarchy = 'date_creation'
    readonly_fields = ('date_creation',)
# Register your models here.

@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ('nom', 'entreprise', 'prix', 'stock', 'categorie', 'disponibilite', 'date_ajout')
    list_filter = ('disponibilite', 'categorie', 'entreprise')
    search_fields = ('nom', 'entreprise__nom')
    ordering = ('nom',)
    date_hierarchy = 'date_ajout'
    readonly_fields = ('date_ajout',)

@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ('entreprise', 'client', 'produit', 'quantite', 'date_commande', 'statut')
    list_filter = ('statut', 'date_commande')
    search_fields = ('entreprise__nom', 'client__nom', 'produit__nom')
    ordering = ('-date_commande',)
    date_hierarchy = 'date_commande'
    readonly_fields = ('date_commande',)
# Register your models here